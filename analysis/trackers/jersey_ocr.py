# app/trackers/jersey_ocr.py
# Deteksi nomor punggung otomatis menggunakan EasyOCR (GPU) + Temporal Majority Voting
# Cocok untuk video latihan dengan 2-3 pemain

import cv2
import numpy as np
import logging
import re
import time
from typing import Dict, List, Optional, Tuple, Any

logger = logging.getLogger(__name__)

# Lazy-load EasyOCR
_ocr_instance = None


def _get_ocr():
    """Lazy-initialize EasyOCR dengan GPU (CUDA)."""
    global _ocr_instance
    if _ocr_instance is None:
        try:
            import importlib
            easyocr = importlib.import_module("easyocr")
            print("[JerseyOCR] Initializing EasyOCR (GPU=True)...")
            t0 = time.time()
            _ocr_instance = easyocr.Reader(['en'], gpu=True)
            t1 = time.time()
            print(f"[JerseyOCR] EasyOCR ready in {t1-t0:.1f}s (GPU)")
        except Exception as e:
            print(f"[JerseyOCR] ERROR: EasyOCR init failed: {e}")
            print("[JerseyOCR] Install: pip install easyocr")
            raise
    return _ocr_instance


class JerseyOCR:
    """
    Deteksi nomor punggung pemain dari video menggunakan EasyOCR + GPU.

    Pipeline:
    1. Crop bagian torso dari bounding box pemain
    2. Preprocessing: upscale, CLAHE contrast, threshold
    3. EasyOCR: baca digit (digits-only allowlist)
    4. Temporal majority voting — kumpulkan hasil dari banyak frame, ambil angka terbanyak
    """

    def __init__(
        self,
        torso_top_ratio: float = 0.20,
        torso_bottom_ratio: float = 0.70,
        min_crop_size: int = 20,
        upscale_factor: int = 3,
        sample_every_n_frames: int = 10,
        min_confidence: float = 0.3,
        min_votes: int = 2,
        max_votes_per_track: int = 15,
        max_scan_frames: int = 300,
        valid_jersey_range: Tuple[int, int] = (1, 99),
    ):
        self.torso_top_ratio = torso_top_ratio
        self.torso_bottom_ratio = torso_bottom_ratio
        self.min_crop_size = min_crop_size
        self.upscale_factor = upscale_factor
        self.sample_every_n_frames = sample_every_n_frames
        self.min_confidence = min_confidence
        self.min_votes = min_votes
        self.max_votes_per_track = max_votes_per_track
        self.max_scan_frames = max_scan_frames
        self.valid_range = valid_jersey_range
        self._votes: Dict[int, List[Tuple[int, float]]] = {}

        print(
            f"[JerseyOCR] Config: torso={torso_top_ratio:.0%}-{torso_bottom_ratio:.0%}, "
            f"upscale={upscale_factor}x, sample_every={sample_every_n_frames}, "
            f"max_scan={max_scan_frames}, GPU=True"
        )

    def crop_torso(self, frame: np.ndarray, bbox: List[float]) -> Optional[np.ndarray]:
        """Crop bagian torso dari bounding box pemain."""
        x1, y1, x2, y2 = map(int, bbox)
        h = y2 - y1
        w = x2 - x1
        if h < self.min_crop_size or w < self.min_crop_size:
            return None

        crop_y1 = max(0, y1 + int(h * self.torso_top_ratio))
        crop_y2 = min(frame.shape[0], y1 + int(h * self.torso_bottom_ratio))
        margin_x = int(w * 0.1)
        crop_x1 = max(0, x1 + margin_x)
        crop_x2 = min(frame.shape[1], x2 - margin_x)

        if crop_y2 <= crop_y1 or crop_x2 <= crop_x1:
            return None
        crop = frame[crop_y1:crop_y2, crop_x1:crop_x2]
        if crop.shape[0] < 5 or crop.shape[1] < 5:
            return None
        return crop

    def preprocess(self, crop: np.ndarray) -> np.ndarray:
        """
        Preprocessing untuk OCR:
        - Upscale (memperbesar agar digit lebih jelas)
        - CLAHE (enhance kontras lokal)
        - Sharpen (mempertajam edge digit)
        - Denoise (kurangi noise — pakai GPU jadi cepat)
        """
        h, w = crop.shape[:2]

        # 1. Upscale
        crop = cv2.resize(
            crop,
            (w * self.upscale_factor, h * self.upscale_factor),
            interpolation=cv2.INTER_CUBIC
        )

        # 2. Grayscale + CLAHE
        gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(4, 4))
        gray = clahe.apply(gray)

        # 3. Sharpen
        kernel = np.array([[-1, -1, -1],
                           [-1,  9, -1],
                           [-1, -1, -1]])
        gray = cv2.filter2D(gray, -1, kernel)

        # 4. Convert back to BGR (EasyOCR accepts both gray and BGR)
        return cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)

    def _extract_jersey_number(self, text: str) -> Optional[int]:
        """Ekstrak angka jersey (1-99) dari text OCR."""
        digits = re.sub(r'[^0-9]', '', text.strip())
        if not digits:
            return None
        # Coba full number dulu
        try:
            num = int(digits)
            if self.valid_range[0] <= num <= self.valid_range[1]:
                return num
        except ValueError:
            pass
        # Coba 2 digit pertama
        if len(digits) >= 2:
            try:
                num = int(digits[:2])
                if self.valid_range[0] <= num <= self.valid_range[1]:
                    return num
            except ValueError:
                pass
        # Coba 1 digit
        if len(digits) >= 1:
            try:
                num = int(digits[0])
                if self.valid_range[0] <= num <= self.valid_range[1]:
                    return num
            except ValueError:
                pass
        return None

    def read_number_from_crop(self, crop: np.ndarray) -> Optional[Tuple[int, float]]:
        """Jalankan EasyOCR pada crop image, return (jersey_number, confidence)."""
        reader = _get_ocr()
        processed = self.preprocess(crop)

        try:
            t0 = time.time()
            results = reader.readtext(
                processed,
                allowlist='0123456789',
                paragraph=False,
                detail=1,           # return [bbox, text, confidence]
                min_size=10,
                text_threshold=0.4,
                low_text=0.3,
            )
            elapsed = time.time() - t0

            best_number = None
            best_conf = 0.0

            for (bbox, text, conf) in results:
                if conf < self.min_confidence:
                    continue

                number = self._extract_jersey_number(text)
                if number is not None and conf > best_conf:
                    best_number = number
                    best_conf = conf

            if best_number is not None:
                return (best_number, best_conf)

        except Exception as e:
            print(f"[JerseyOCR] OCR error: {e}")

        return None

    def scan_frames(
        self,
        frames: List[np.ndarray],
        player_tracks: List[Dict[int, Dict]],
        debug: bool = False
    ) -> Dict[int, str]:
        """Scan jersey number dari frames untuk semua track ID."""
        self._votes = {}
        total_frames = min(len(frames), self.max_scan_frames)
        scanned = 0
        detected = 0

        print(f"[JerseyOCR] Scanning first {total_frames} frames "
              f"(every {self.sample_every_n_frames} frames)...")

        scan_start = time.time()

        for frame_idx in range(0, total_frames, self.sample_every_n_frames):
            if frame_idx >= len(player_tracks):
                break

            frame = frames[frame_idx]
            players_in_frame = player_tracks[frame_idx]

            for track_id, player_data in players_in_frame.items():
                # Skip jika track sudah punya cukup votes
                if track_id in self._votes and len(self._votes[track_id]) >= self.max_votes_per_track:
                    continue

                bbox = player_data.get('bbox')
                if bbox is None:
                    continue

                crop = self.crop_torso(frame, bbox)
                if crop is None:
                    continue

                scanned += 1
                result = self.read_number_from_crop(crop)
                if result is not None:
                    number, conf = result
                    if track_id not in self._votes:
                        self._votes[track_id] = []
                    self._votes[track_id].append((number, conf))
                    detected += 1

                    if debug and len(self._votes[track_id]) <= 3:
                        print(
                            f"[JerseyOCR] Frame {frame_idx}: "
                            f"Track {track_id} -> #{number} (conf={conf:.2f})"
                        )

            # Progress log
            if frame_idx % (self.sample_every_n_frames * 10) == 0:
                print(
                    f"[JerseyOCR] Progress: frame {frame_idx}/{total_frames}, "
                    f"scanned={scanned}, detected={detected}"
                )

            # Early exit jika semua track sudah punya cukup votes
            if (self._votes and
                all(len(v) >= self.max_votes_per_track for v in self._votes.values())):
                print(f"[JerseyOCR] Early exit: all tracks have enough votes")
                break

        scan_elapsed = time.time() - scan_start
        print(f"[JerseyOCR] Scan complete in {scan_elapsed:.1f}s. "
              f"Scanned={scanned}, Detected={detected}")
        return self._majority_vote(debug=debug)

    def _majority_vote(self, debug: bool = False) -> Dict[int, str]:
        """Temporal majority voting per track ID."""
        result: Dict[int, str] = {}

        for track_id, votes in self._votes.items():
            if len(votes) < self.min_votes:
                if debug:
                    print(f"[JerseyOCR] Track {track_id}: {len(votes)} votes (skip)")
                continue

            # Weighted voting: confidence sebagai bobot
            number_counts: Dict[int, float] = {}
            for number, conf in votes:
                number_counts[number] = number_counts.get(number, 0) + conf

            best_number = max(number_counts, key=number_counts.get)
            total_votes = len(votes)
            best_count = sum(1 for n, _ in votes if n == best_number)
            ratio = best_count / total_votes

            if ratio >= 0.3:  # Minimal 30% votes harus sama
                result[track_id] = f"#{best_number}"
                if debug:
                    print(f"[JerseyOCR] Track {track_id} -> #{best_number} "
                          f"({best_count}/{total_votes} = {ratio:.0%})")

        print(f"[JerseyOCR] Final mapping: {result}")
        return result


# ==============================================================================
# PaddleOCR Backend
# ==============================================================================

_paddle_ocr_instance = None


def _get_paddle_ocr():
    """Lazy-initialize PaddleOCR dengan GPU (CUDA)."""
    global _paddle_ocr_instance
    if _paddle_ocr_instance is None:
        try:
            import importlib
            PaddleOCR = importlib.import_module("paddleocr").PaddleOCR
            torch = importlib.import_module("torch")
            use_gpu = torch.cuda.is_available()

            # Set device sebelum init (PaddleOCR 2.8+ tidak pakai use_gpu param)
            try:
                paddle = importlib.import_module("paddle")
                paddle.device.set_device('gpu' if use_gpu else 'cpu')
            except Exception:
                pass  # fallback: biarkan PaddleOCR auto-detect

            print(f"[JerseyOCR-Paddle] Initializing PaddleOCR (GPU={use_gpu})...")
            t0 = time.time()
            _paddle_ocr_instance = PaddleOCR(
                use_angle_cls=False,
                lang='en',
                show_log=False,
            )
            t1 = time.time()
            gpu_label = "GPU (CUDA)" if use_gpu else "CPU"
            print(f"[JerseyOCR-Paddle] PaddleOCR ready in {t1-t0:.1f}s ({gpu_label})")
        except Exception as e:
            print(f"[JerseyOCR-Paddle] ERROR: PaddleOCR init failed: {e}")
            print("[JerseyOCR-Paddle] Install: pip install paddlepaddle-gpu paddleocr")
            raise
    return _paddle_ocr_instance


class JerseyOCRPaddle(JerseyOCR):
    """
    Deteksi nomor punggung pemain menggunakan PaddleOCR + GPU.

    Mewarisi semua logic dari JerseyOCR (crop_torso, preprocess,
    _extract_jersey_number, scan_frames, _majority_vote).
    Hanya override read_number_from_crop() untuk menggunakan PaddleOCR.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        print("[JerseyOCR-Paddle] Using PaddleOCR engine (GPU enabled)")

    def read_number_from_crop(self, crop: np.ndarray) -> Optional[Tuple[int, float]]:
        """Jalankan PaddleOCR pada crop image, return (jersey_number, confidence)."""
        ocr = _get_paddle_ocr()
        processed = self.preprocess(crop)

        # PaddleOCR expects BGR numpy array
        # Convert preprocessed (which is BGR from cv2.cvtColor) — already correct
        try:
            t0 = time.time()
            results = ocr.ocr(processed, cls=False)
            elapsed = time.time() - t0

            best_number = None
            best_conf = 0.0

            if results and results[0]:
                for line in results[0]:
                    # PaddleOCR format: [bbox, (text, confidence)]
                    if len(line) < 2:
                        continue
                    text_info = line[1]
                    if isinstance(text_info, tuple) and len(text_info) >= 2:
                        text, conf = text_info[0], text_info[1]
                    else:
                        continue

                    if conf < self.min_confidence:
                        continue

                    number = self._extract_jersey_number(str(text))
                    if number is not None and conf > best_conf:
                        best_number = number
                        best_conf = conf

            if best_number is not None:
                return (best_number, best_conf)

        except Exception as e:
            print(f"[JerseyOCR-Paddle] OCR error: {e}")

        return None


# ==============================================================================
# Factory Function
# ==============================================================================

def create_jersey_ocr(engine: str = 'easyocr', **kwargs) -> JerseyOCR:
    """
    Factory function untuk membuat instance JerseyOCR sesuai pilihan engine.

    Args:
        engine: 'easyocr' atau 'paddleocr'
        **kwargs: parameter yang diteruskan ke constructor JerseyOCR/JerseyOCRPaddle

    Returns:
        Instance JerseyOCR (EasyOCR) atau JerseyOCRPaddle (PaddleOCR)
    """
    engine = engine.lower().strip()
    if engine == 'paddleocr':
        print(f"[JerseyOCR] Creating PaddleOCR engine")
        return JerseyOCRPaddle(**kwargs)
    else:
        print(f"[JerseyOCR] Creating EasyOCR engine")
        return JerseyOCR(**kwargs)
