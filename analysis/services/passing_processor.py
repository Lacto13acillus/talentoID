# app/services/passing_processor.py
# Pipeline utama passing analytics dengan static/auto player identification
import os, sys, cv2, logging, subprocess
import numpy as np
from typing import Dict, List, Optional, Any

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if PROJECT_ROOT not in sys.path: sys.path.insert(0, PROJECT_ROOT)

from analysis.trackers.tracker import Tracker
from analysis.trackers.player_identifier import PlayerIdentifier
from analysis.trackers.player_ball_assigner import PlayerBallAssigner
from analysis.trackers.pass_detector import PassDetector
from analysis.trackers.jersey_ocr import JerseyOCR, create_jersey_ocr
from analysis.utils.draw_gate import (
    draw_target_cone_on_frame, draw_ball_trajectory_on_frame,
    draw_pass_arrow, draw_stats_panel
)
from analysis.utils.bbox_utils import get_center_of_bbox

logger = logging.getLogger(__name__)


def _ensure_browser_compatible(video_path: str) -> bool:
    """Konversi video ke H.264 + yuv420p + faststart agar bisa diputar di browser."""
    if not os.path.exists(video_path):
        return False
    temp_path = video_path.replace('.mp4', '_browser_tmp.mp4')
    try:
        subprocess.run(['ffmpeg', '-version'], stdout=subprocess.DEVNULL,
                       stderr=subprocess.DEVNULL, check=True)
    except FileNotFoundError:
        logger.warning("[FFmpeg] ffmpeg tidak ditemukan")
        return False
    try:
        result = subprocess.run(
            ['ffmpeg', '-y', '-i', video_path, '-c:v', 'libx264', '-preset', 'fast',
             '-crf', '23', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', '-an', temp_path],
            capture_output=True, text=True, timeout=600
        )
        if result.returncode == 0 and os.path.exists(temp_path) and os.path.getsize(temp_path) > 0:
            os.replace(temp_path, video_path)
            logger.info(f"[FFmpeg] OK → browser-compatible: {video_path}")
            return True
        else:
            logger.warning(f"[FFmpeg] Gagal (rc={result.returncode})")
            if os.path.exists(temp_path):
                os.remove(temp_path)
            return False
    except Exception as e:
        logger.error(f"[FFmpeg] Error: {e}")
        if os.path.exists(temp_path):
            os.remove(temp_path)
        return False


def _build_jersey_to_name_map(jersey_mapping: Dict, player_names: List[str]) -> Dict[str, str]:
    """
    Buat mapping jersey → nama pemain.
    Ambil jersey unik (non-Unknown) dari jersey_mapping, urutkan,
    lalu map ke player_names secara berurutan.

    Contoh:
        jersey_mapping = {1: "#3", 2: "#19", 3: "Unknown", ...}
        player_names = ["Andi", "Budi"]
        → {"#3": "Andi", "#19": "Budi"}
    """
    unique_jerseys = sorted(set(
        v for v in jersey_mapping.values() if v != "Unknown"
    ))
    mapping = {}
    for i, jersey in enumerate(unique_jerseys):
        if i < len(player_names):
            mapping[jersey] = player_names[i]
        else:
            mapping[jersey] = jersey  # fallback ke jersey number
    print(f"[PASSING] Jersey → Name mapping: {mapping}")
    return mapping


def _map_player_names_to_passes(passes: List[Dict], player_names: List[str],
                                 jersey_mapping: Dict = None) -> List[Dict]:
    """
    Map nama pemain ke pass events berdasarkan jersey ID.
    Nama pertama menempel ke jersey pertama (#3), nama kedua ke jersey kedua (#19), dst.
    """
    if not player_names or not jersey_mapping:
        return passes
    j2n = _build_jersey_to_name_map(jersey_mapping, player_names)
    for p in passes:
        jersey = p.get('from_jersey', '')
        p['sender_name'] = j2n.get(jersey, jersey)
    return passes


def _compute_named_stats(passes: List[Dict]) -> Dict:
    """Hitung statistik dengan nama pemain (bukan jersey)."""
    total = len(passes)
    sukses = [p for p in passes if p['success']]
    gagal = [p for p in passes if not p['success']]

    per_player: Dict[str, Dict] = {}
    for p in passes:
        name = p.get('sender_name', p.get('from_jersey', 'Unknown'))
        if name not in per_player:
            per_player[name] = {'total': 0, 'success': 0, 'failed': 0,
                                'accuracy_pct': 0.0, 'avg_closest': 0.0, '_cs': 0.0}
        per_player[name]['total'] += 1
        per_player[name]['_cs'] += p.get('closest_dist', 0.0)
        if p['success']:
            per_player[name]['success'] += 1
        else:
            per_player[name]['failed'] += 1

    for name, s in per_player.items():
        s['accuracy_pct'] = round(s['success'] / s['total'] * 100, 1) if s['total'] > 0 else 0.0
        s['avg_closest'] = round(s['_cs'] / s['total'], 1) if s['total'] > 0 else 0.0
        del s['_cs']

    return {
        'total_passes': total,
        'successful_passes': len(sukses),
        'failed_passes': len(gagal),
        'accuracy_pct': round(len(sukses) / total * 100, 1) if total > 0 else 0.0,
        'per_player': per_player
    }


def _compute_progressive_named_stats(passes: List[Dict], up_to_frame: int) -> Dict:
    """Stats kumulatif sampai frame tertentu, menggunakan nama pemain."""
    so_far = [p for p in passes if p['frame_display'] <= up_to_frame]
    return _compute_named_stats(so_far)


def _render_passing_frames(frames, tracks, ball_possessions, passes,
                           player_identifier, pass_detector, config,
                           detection_mode='manual', jersey_to_name=None):
    """Render semua frame dengan annotasi passing."""
    out_frames = []
    total = len(frames)
    pass_map = {p['frame_display']: p for p in passes}
    rolling_traj = []

    for i, frame in enumerate(frames):
        out = frame.copy()

        # Target cone
        ti = pass_detector.get_target_cone()
        if ti and config.get('show_target_cone', True):
            _, tpos = ti
            radius = config.get('target_proximity_radius', 120.0)
            active = any(p['frame_start'] <= i <= p['frame_end'] and p['success'] for p in passes)
            out = draw_target_cone_on_frame(out, tpos, radius, active)

        # Player bounding boxes
        for pid, pd in tracks['players'][i].items():
            bbox = pd.get('bbox')
            if bbox is None: continue
            x1, y1, x2, y2 = map(int, bbox)
            has_ball = (i < len(ball_possessions) and ball_possessions[i] == pid)
            bc = (0, 200, 50) if has_ball else (200, 80, 50)
            cv2.rectangle(out, (x1, y1), (x2, y2), bc, 2)
            jersey = player_identifier.get_jersey_number_for_player(pid)
            # Show player name if manual mode and mapping exists, else show jersey
            if detection_mode == 'manual' and jersey_to_name and jersey in jersey_to_name:
                label = jersey_to_name[jersey]
            else:
                label = f"#{jersey}"
            (lw, lh), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.55, 1)
            cv2.rectangle(out, (x1, y1-lh-8), (x1+lw+8, y1), bc, -1)
            cv2.putText(out, label, (x1+4, y1-4), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255,255,255), 1)
            if has_ball:
                fx, fy = (x1+x2)//2, y2
                cv2.circle(out, (fx, fy), 8, (0,230,255), -1)
                cv2.circle(out, (fx, fy), 11, (255,255,255), 2)

        # Ball
        bd = tracks['ball'][i].get(1)
        if bd and 'bbox' in bd:
            bx1, by1, bx2, by2 = map(int, bd['bbox'])
            bcx, bcy = (bx1+bx2)//2, (by1+by2)//2
            br = max(8, (bx2-bx1)//2)
            cv2.circle(out, (bcx, bcy), br, (0,230,255), 2)
            if config.get('debug_trajectory', False):
                rolling_traj.append((bcx, bcy))
                if len(rolling_traj) > 45: rolling_traj.pop(0)

        if config.get('debug_trajectory', False) and len(rolling_traj) > 1:
            out = draw_ball_trajectory_on_frame(out, rolling_traj, max_points=30)

        # Pass arrow - use sender_name instead of jersey
        if config.get('show_pass_arrows', True) and i in pass_map:
            pe = pass_map[i]
            from_label = pe.get('sender_name', pe['from_jersey'])
            to_label = pe.get('to_jersey', '?')
            out = draw_pass_arrow(out, pe['from_pos'], pe['to_pos'],
                                  pe['success'], from_label, to_label, pe['distance'])

        # Stats panel
        if config.get('show_stats_panel', True):
            rt_stats = _compute_progressive_named_stats(passes, i)
            out = draw_stats_panel(out, rt_stats, (20, 20), 295)

        # Frame label
        h, w = out.shape[:2]
        cv2.putText(out, f"Frame: {i}", (w-140, h-10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.42, (110,110,110), 1)
        out_frames.append(out)

    return out_frames


def run_passing_pipeline(input_path, output_path, job_id, model_path,
                         player_names=None, detection_mode='manual',
                         ocr_engine='easyocr',
                         fps=30, use_stub=False,
                         stub_path=None, config_overrides=None):
    """
    Pipeline utama passing analytics.

    Args:
        player_names: list nama pemain untuk mapping urutan pass (mode manual)
        detection_mode: 'manual' atau 'auto'
            - 'manual': user input nama, di-map ke jersey number
            - 'auto': langsung pakai jersey number sebagai identifier
        ocr_engine: 'easyocr' atau 'paddleocr' (hanya untuk mode auto)
    """
    result = {
        'job_id': job_id, 'status': 'processing', 'progress': 0,
        'stats': None, 'pass_events': [], 'output_video': None, 'error': None
    }

    cfg = {
        'jersey_mapping': {1: "#3", 2: "#19", 3: "Unknown", 4: "#3",
                           5: "#19", 6: "Unknown", 7: "Unknown"},
        'reassign_distance_threshold': 150.0,
        'lost_timeout_frames': 60,
        'manual_target_cone_id': None,
        'target_selection_mode': 'highest',
        'target_proximity_radius': 100,
        'max_possession_distance': 130,
        'show_target_cone': True,
        'debug_trajectory': False,
        'show_pass_arrows': True,
        'show_stats_panel': True,
        'output_format': 'mp4',
        **(config_overrides or {})
    }

    if player_names is None:
        player_names = []

    logger.info(f"[{job_id}] Detection mode: {detection_mode}, OCR engine: {ocr_engine}")

    try:
        # TAHAP 1: Baca Video
        logger.info(f"[{job_id}] Reading video: {input_path}")
        frames = Tracker.read_video(input_path)
        if not frames:
            raise ValueError("Video empty or unreadable")
        result['progress'] = 5

        # TAHAP 2: Deteksi & Tracking
        logger.info(f"[{job_id}] Running YOLO tracking...")
        tracker = Tracker(model_path=model_path, model_type='passing')
        if not stub_path:
            stub_path = os.path.join(PROJECT_ROOT, 'static', 'stubs', f"{job_id}_tracks.pkl")
            os.makedirs(os.path.dirname(stub_path), exist_ok=True)
        tracks = tracker.get_object_tracks(frames, read_from_stub=use_stub, stub_path=stub_path)
        result['progress'] = 25

        n_pf = len(tracks.get('players', []))
        n_bf = len(tracks.get('ball', []))
        if n_pf == 0 or n_bf == 0:
            raise ValueError("Tracking failed - no players or ball detected")

        # TAHAP 3: Jersey Identification
        ocr_jersey_map = None  # Will be set in auto mode

        if detection_mode == 'auto':
            # AUTO MODE: Scan jersey numbers dari video menggunakan OCR
            print(f"[{job_id}] Auto mode — scanning jersey numbers with {ocr_engine}...")
            dynamic_mapping = {}
            try:
                jersey_ocr = create_jersey_ocr(
                    engine=ocr_engine,
                    torso_top_ratio=0.20,
                    torso_bottom_ratio=0.70,
                    upscale_factor=3,
                    sample_every_n_frames=10,
                    min_confidence=0.3,
                    min_votes=2,
                    max_votes_per_track=15,
                    max_scan_frames=300,
                )
                ocr_jersey_map = jersey_ocr.scan_frames(
                    frames, tracks['players'], debug=True
                )
                for tid, jersey_str in ocr_jersey_map.items():
                    dynamic_mapping[tid] = jersey_str
                print(f"[{job_id}] OCR jersey mapping: {dynamic_mapping}")
            except Exception as e:
                # Fallback: gunakan track ID sebagai identifier
                print(f"[{job_id}] OCR failed ({e}), using track IDs as fallback")
                # Kumpulkan semua unique track IDs
                all_tids = set()
                for frame_players in tracks['players']:
                    all_tids.update(frame_players.keys())
                for i, tid in enumerate(sorted(all_tids)):
                    dynamic_mapping[tid] = f"Pemain {i+1}"
                print(f"[{job_id}] Fallback mapping: {dynamic_mapping}")

            result['progress'] = 30

            pi = PlayerIdentifier(
                track_id_to_jersey=dynamic_mapping,
                reassign_distance_threshold=cfg['reassign_distance_threshold'],
                lost_timeout_frames=cfg['lost_timeout_frames']
            )
        else:
            # MANUAL MODE: Gunakan static mapping dari config
            print(f"[{job_id}] Manual mode — using static jersey mapping")
            pi = PlayerIdentifier(
                track_id_to_jersey=cfg['jersey_mapping'],
                reassign_distance_threshold=cfg['reassign_distance_threshold'],
                lost_timeout_frames=cfg['lost_timeout_frames']
            )

        for fn in range(n_pf):
            pi.update_frame(fn, tracks['players'][fn], debug=(fn % 100 == 0))
        result['progress'] = 35

        # TAHAP 4: Pass Detector + Target Cone
        logger.info(f"[{job_id}] Initializing pass detector...")
        pd = PassDetector(fps=fps)
        pd.set_jersey_map(pi)

        # Set allowed_jerseys dynamically berdasarkan detection mode
        if detection_mode == 'auto' and ocr_jersey_map:
            # Auto mode: ambil semua jersey unik dari OCR results
            detected_jerseys = set(ocr_jersey_map.values())
            pd.set_allowed_jerseys(detected_jerseys)
            logger.info(f"[{job_id}] Auto mode allowed jerseys: {detected_jerseys}")
        else:
            # Manual mode: ambil semua jersey non-Unknown dari static mapping
            known_jerseys = set(
                v for v in cfg.get('jersey_mapping', {}).values()
                if v != "Unknown"
            )
            pd.set_allowed_jerseys(known_jerseys)
            logger.info(f"[{job_id}] Manual mode allowed jerseys: {known_jerseys}")
        pd.manual_target_cone_id = cfg.get('manual_target_cone_id')
        pd.target_selection_mode = cfg.get('target_selection_mode', 'highest')
        pd.target_proximity_radius = cfg.get('target_proximity_radius', 120.0)
        pd.initialize_target_cone(tracks, cone_key='cones', sample_frames=30, debug=True)
        result['progress'] = 40

        # TAHAP 5: Ball Possession
        logger.info(f"[{job_id}] Ball possession assignment...")
        assigner = PlayerBallAssigner(
            max_possession_distance=cfg.get('max_possession_distance', 130.0)
        )
        assigner.set_player_identifier(pi)
        ball_poss = assigner.assign_ball_to_players_bulk(tracks)
        result['progress'] = 55

        # TAHAP 6: Detect Passes
        logger.info(f"[{job_id}] Detecting passes...")
        passes = pd.detect_passes(tracks, ball_poss, player_identifier=pi, debug=True)
        result['progress'] = 65

        # TAHAP 7: Map Player Names to Passes
        jersey_to_name = None
        if detection_mode == 'auto':
            # Auto mode: jersey number dari OCR langsung jadi identifier
            logger.info(f"[{job_id}] Auto mode — using OCR jersey numbers as player IDs")
            for p in passes:
                jersey = p.get('from_jersey', '')
                # Jersey sudah dalam format "#3" dari PlayerIdentifier
                p['sender_name'] = jersey if jersey.startswith('#') else f"#{jersey}"
        else:
            # Manual mode: map nama pemain ke jersey number
            passes = _map_player_names_to_passes(passes, player_names, jersey_mapping=cfg.get('jersey_mapping'))
            jersey_to_name = _build_jersey_to_name_map(cfg.get('jersey_mapping', {}), player_names)

        # Compute stats with player names / jersey numbers
        stats = _compute_named_stats(passes)
        result['stats'] = stats
        result['pass_events'] = passes
        result['progress'] = 70

        # TAHAP 8: Render Video
        logger.info(f"[{job_id}] Rendering video with annotations...")
        out_frames = _render_passing_frames(
            frames, tracks, ball_poss, passes, pi, pd, cfg,
            detection_mode=detection_mode,
            jersey_to_name=jersey_to_name
        )
        result['progress'] = 90

        # TAHAP 9: Save Video
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        fourcc = 'mp4v' if cfg.get('output_format') == 'mp4' else 'XVID'
        Tracker.save_video(out_frames, output_path, fps=fps, fourcc=fourcc)

        # TAHAP 10: Konversi ke H.264 + yuv420p + faststart agar bisa diputar di browser
        converted = _ensure_browser_compatible(output_path)
        if not converted:
            logger.warning(f"[{job_id}] ffmpeg konversi gagal, video mungkin tidak bisa diputar di browser")

        result['output_video'] = output_path
        result['progress'] = 100
        result['status'] = 'completed'
        logger.info(f"[{job_id}] Done. {stats['total_passes']} passes detected.")

    except Exception as e:
        logger.error(f"[{job_id}] Failed: {str(e)}", exc_info=True)
        result['status'] = 'failed'
        result['error'] = str(e)

    return result
