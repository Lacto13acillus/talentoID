# app/trackers/player_ball_assigner.py
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from analysis.utils.bbox_utils import measure_distance, get_center_of_bbox, get_foot_position
from typing import Dict, List, Any, Optional, Tuple
import numpy as np

class PlayerBallAssigner:
    def __init__(self, max_possession_distance=70.0, foot_region_ratio=0.3,
                 player_identifier=None, jersey_priority_bonus=0.70):
        self.max_possession_distance = max_possession_distance
        self.foot_region_ratio = foot_region_ratio
        self._player_identifier = player_identifier
        self.jersey_priority_bonus = jersey_priority_bonus
        self.priority_jerseys = {"#3", "#19"}

    def set_player_identifier(self, pi): self._player_identifier = pi

    def _get_foot_region_center(self, bbox):
        x1,y1,x2,y2 = bbox
        bh = y2-y1; fy = y2-(bh*self.foot_region_ratio*0.5); cx=(x1+x2)/2
        return int(cx), int(fy)

    def assign_ball_to_player(self, players, ball_bbox):
        if ball_bbox is None or not players: return -1
        ball_pos = np.array(get_center_of_bbox(ball_bbox), dtype=np.float32)
        cands = []
        for pid, pd in players.items():
            pb = pd.get('bbox')
            if pb is None: continue
            fp = np.array(self._get_foot_region_center(pb), dtype=np.float32)
            d = float(np.linalg.norm(ball_pos - fp))
            ed = d
            if self._player_identifier:
                j = self._player_identifier.get_jersey_number_for_player(pid)
                if j in self.priority_jerseys: ed = d * self.jersey_priority_bonus
            cands.append((pid, d, ed))
        if not cands: return -1
        cands.sort(key=lambda x: x[2])
        best_pid, best_d, _ = cands[0]
        return best_pid if best_d <= self.max_possession_distance else -1

    def assign_ball_to_players_bulk(self, tracks, debug_interval=100):
        total = len(tracks['players']); poss = []; pc = 0
        for f in range(total):
            if f % debug_interval == 0: print(f"[ASSIGNER] Frame {f}/{total}...")
            pl = tracks['players'][f]
            bf = tracks['ball'][f].get(1)
            bb = bf['bbox'] if bf else None
            a = self.assign_ball_to_player(pl, bb); poss.append(a)
            if a != -1: pc += 1
        pct = pc/total*100 if total > 0 else 0
        print(f"\n[ASSIGNER] Done: {pc}/{total} frames with possession ({pct:.1f}%)")
        return poss
