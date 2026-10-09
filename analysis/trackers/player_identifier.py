# app/trackers/player_identifier.py
# Memetakan ByteTrack ID ke nomor Jersey (#3, #19, Unknown)
# V2: Dynamic Spatial Re-Identification

from typing import Dict, Optional, Tuple, List
import numpy as np


class PlayerIdentifier:
    def __init__(
        self,
        track_id_to_jersey: Optional[Dict[int, str]] = None,
        reassign_distance_threshold: float = 150.0,
        lost_timeout_frames: int = 60
    ):
        self._track_to_jersey: Dict[int, str] = {}
        self._jersey_to_tracks: Dict[str, List[int]] = {}
        self._last_positions: Dict[int, Tuple[float, float]] = {}
        self._last_seen_frame: Dict[int, int] = {}
        self._active_track_per_jersey: Dict[str, int] = {}
        self._reassign_threshold = reassign_distance_threshold
        self._lost_timeout = lost_timeout_frames

        if track_id_to_jersey:
            for tid, jersey in track_id_to_jersey.items():
                self._register_mapping(tid, jersey)

        print(f"[IDENTIFIER] Mapping jersey dimuat: {self._track_to_jersey}")
        print(f"[IDENTIFIER] Reassign threshold: {self._reassign_threshold}px")
        print(f"[IDENTIFIER] Lost timeout: {self._lost_timeout} frames")

    def _register_mapping(self, track_id: int, jersey: str) -> None:
        self._track_to_jersey[track_id] = jersey
        if jersey not in self._jersey_to_tracks:
            self._jersey_to_tracks[jersey] = []
        if track_id not in self._jersey_to_tracks[jersey]:
            self._jersey_to_tracks[jersey].append(track_id)
        self._active_track_per_jersey[jersey] = track_id

    @staticmethod
    def _distance(p1: Tuple[float, float], p2: Tuple[float, float]) -> float:
        return float(np.linalg.norm(
            np.array(p1, dtype=np.float32) - np.array(p2, dtype=np.float32)
        ))

    def update_frame(
        self,
        frame_num: int,
        player_tracks: Dict[int, Dict],
        debug: bool = False
    ) -> None:
        current_track_ids = set(player_tracks.keys())

        for tid, data in player_tracks.items():
            bbox = data.get('bbox')
            if bbox is None:
                continue
            cx = (bbox[0] + bbox[2]) / 2
            cy = bbox[3]
            self._last_positions[tid] = (cx, cy)
            self._last_seen_frame[tid] = frame_num

        new_track_ids = [
            tid for tid in current_track_ids
            if tid not in self._track_to_jersey
        ]

        if not new_track_ids:
            return

        lost_jerseys: Dict[str, Tuple[float, float]] = {}

        for jersey, active_tid in list(self._active_track_per_jersey.items()):
            if jersey == "Unknown":
                continue
            if active_tid in current_track_ids:
                continue
            last_frame = self._last_seen_frame.get(active_tid, -999)
            frames_since_lost = frame_num - last_frame
            if frames_since_lost > self._lost_timeout:
                continue
            last_pos = self._last_positions.get(active_tid)
            if last_pos is not None:
                lost_jerseys[jersey] = last_pos

        if not lost_jerseys:
            for tid in new_track_ids:
                if tid not in self._track_to_jersey:
                    self._register_mapping(tid, "Unknown")
                    if debug:
                        print(f"[IDENTIFIER] Frame {frame_num}: "
                              f"Track {tid} -> Unknown (tidak ada jersey hilang)")
            return

        assignments: List[Tuple[int, str, float]] = []

        for tid in new_track_ids:
            pos = self._last_positions.get(tid)
            if pos is None:
                continue
            best_jersey = None
            best_dist = float('inf')
            for jersey, lost_pos in lost_jerseys.items():
                dist = self._distance(pos, lost_pos)
                if dist < best_dist:
                    best_dist = dist
                    best_jersey = jersey
            if best_jersey and best_dist <= self._reassign_threshold:
                assignments.append((tid, best_jersey, best_dist))

        assignments.sort(key=lambda x: x[2])
        assigned_jerseys = set()

        for tid, jersey, dist in assignments:
            if jersey in assigned_jerseys:
                continue
            self._register_mapping(tid, jersey)
            assigned_jerseys.add(jersey)
            if debug:
                print(f"[IDENTIFIER] Frame {frame_num}: "
                      f"RE-ID Track {tid} -> {jersey} "
                      f"(jarak={dist:.0f}px)")

        for tid in new_track_ids:
            if tid not in self._track_to_jersey:
                self._register_mapping(tid, "Unknown")
                if debug:
                    print(f"[IDENTIFIER] Frame {frame_num}: "
                          f"Track {tid} -> Unknown (tidak cocok)")

    def set_mapping(self, track_id: int, jersey: str) -> None:
        self._register_mapping(track_id, jersey)
        print(f"[IDENTIFIER] Mapping manual: Track ID {track_id} -> Jersey {jersey}")

    def get_jersey_number_for_player(self, track_id: int) -> str:
        return self._track_to_jersey.get(track_id, f"ID:{track_id}")

    def get_track_id_for_jersey(self, jersey: str) -> Optional[int]:
        return self._active_track_per_jersey.get(jersey, None)

    def is_same_player(self, track_id_a: int, track_id_b: int) -> bool:
        jersey_a = self.get_jersey_number_for_player(track_id_a)
        jersey_b = self.get_jersey_number_for_player(track_id_b)
        if jersey_a.startswith("ID:") or jersey_b.startswith("ID:"):
            return track_id_a == track_id_b
        if jersey_a == "Unknown" or jersey_b == "Unknown":
            return track_id_a == track_id_b
        return jersey_a == jersey_b

    def get_all_mappings(self) -> Dict[int, str]:
        return dict(self._track_to_jersey)

    def get_all_track_ids_for_jersey(self, jersey: str) -> List[int]:
        return list(self._jersey_to_tracks.get(jersey, []))

    def print_mappings(self) -> None:
        print("\n[IDENTIFIER] === PLAYER MAPPINGS ===")
        if not self._track_to_jersey:
            print("[IDENTIFIER] Belum ada mapping.")
        for tid, jersey in sorted(self._track_to_jersey.items()):
            active_marker = ""
            if self._active_track_per_jersey.get(jersey) == tid:
                active_marker = " (AKTIF)"
            print(f"[IDENTIFIER]   Track ID {tid:3d} -> Jersey {jersey}{active_marker}")
        print("[IDENTIFIER] ========================\n")
