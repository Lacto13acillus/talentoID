# app/trackers/pass_detector.py
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from analysis.utils.bbox_utils import (
    measure_distance, get_center_of_bbox_bottom, get_center_of_bbox,
    extract_ball_trajectory, stabilize_cone_positions,
    identify_target_cone, check_ball_reached_target_cone
)
import numpy as np
from collections import Counter
from typing import Dict, List, Any, Optional, Tuple


class PassDetector:
    def __init__(self, fps=24):
        self.fps = fps
        self.smoothing_window = 5
        self.min_stable_frames = 1
        self.min_pass_distance = 30
        self.max_pass_distance = 1500
        self.cooldown_frames = 3
        self.min_possession_duration = 1
        self.ball_movement_check_radius = 25
        self.ball_movement_threshold = 4
        self.player_search_radius = 20
        self.pass_display_delay = 3
        self.min_display_gap = 3
        self.allowed_jerseys = None  # None = accept all known jerseys
        self.eval_buffer_before = 0
        self.eval_buffer_after = 15
        self.manual_target_cone_id = None
        self.target_selection_mode = "highest"
        self.target_proximity_radius = 80
        self._target_cone_id = None
        self._target_cone_pos = None
        self._stabilized_cones = None
        self._player_identifier = None

    def set_jersey_map(self, pi): self._player_identifier = pi

    def set_allowed_jerseys(self, jerseys):
        """Set daftar jersey yang boleh mengirim pass.
        Jika None, semua jersey non-Unknown diterima.
        Jika set, hanya jersey dalam set yang dihitung."""
        self.allowed_jerseys = set(jerseys) if jerseys else None
        print(f"[PASS] allowed_jerseys = {self.allowed_jerseys}")

    def _get_jersey(self, pid):
        if self._player_identifier:
            return self._player_identifier.get_jersey_number_for_player(pid)
        return str(pid)

    def get_target_cone(self):
        if self._target_cone_id is None or self._target_cone_pos is None: return None
        return self._target_cone_id, self._target_cone_pos

    def get_all_cones(self): return self._stabilized_cones

    def initialize_target_cone(self, tracks, cone_key='cones', sample_frames=30, debug=True):
        if cone_key not in tracks or not tracks[cone_key]:
            print(f"[TARGET] WARNING: Key '{cone_key}' tidak ada di tracks!")
            return False
        self._stabilized_cones = stabilize_cone_positions(tracks, cone_key=cone_key, sample_frames=sample_frames)
        if len(self._stabilized_cones) == 0:
            print("[TARGET] GAGAL: Tidak ada cone terdeteksi!")
            return False
        result = identify_target_cone(self._stabilized_cones, self.manual_target_cone_id, self.target_selection_mode)
        if result is None:
            print("[TARGET] GAGAL: Tidak bisa mengidentifikasi target cone!")
            return False
        self._target_cone_id, self._target_cone_pos = result
        if debug:
            print(f"[TARGET] Target cone: ID={self._target_cone_id}, pos={self._target_cone_pos}, radius={self.target_proximity_radius}")
        return True

    def evaluate_pass_to_target(self, tracks, pass_event, debug=False):
        if self._target_cone_pos is None:
            return True, "Target cone tidak diinisialisasi - semua pass = SUKSES"
        fs, fe = pass_event['frame_start'], pass_event['frame_end']
        traj = extract_ball_trajectory(tracks, fs, fe, buffer_before=self.eval_buffer_before, buffer_after=self.eval_buffer_after)
        reached, reason = check_ball_reached_target_cone(traj, self._target_cone_pos, self.target_proximity_radius)
        return reached, reason

    def smooth_possessions(self, raw):
        sm = list(raw); hw = self.smoothing_window // 2
        for i in range(hw, len(raw) - hw):
            w = raw[i-hw:i+hw+1]; v = [p for p in w if p != -1]
            sm[i] = Counter(v).most_common(1)[0][0] if v else -1
        return sm

    def fill_short_gaps(self, poss, max_gap=20):
        f = list(poss); lv = -1; gs = -1
        for i in range(len(f)):
            if f[i] != -1:
                if lv != -1 and gs != -1 and (i - gs) <= max_gap:
                    for g in range(gs, i): f[g] = lv
                lv = f[i]; gs = -1
            elif gs == -1: gs = i
        return f

    def _normalize_possessions_by_jersey(self, poss):
        if not self._player_identifier: return poss
        jc = {}; norm = list(poss)
        for i, pid in enumerate(poss):
            if pid == -1: continue
            j = self._get_jersey(pid)
            if j == "Unknown": continue
            if j not in jc: jc[j] = pid
            norm[i] = jc[j]
        return norm

    def get_stable_segments(self, sm):
        segs = []; cp = -1; ss = 0
        for fn, pid in enumerate(sm):
            if pid != cp:
                if cp != -1 and (fn - ss) >= self.min_stable_frames:
                    segs.append({'player_id': cp, 'frame_start': ss, 'frame_end': fn-1})
                cp = pid; ss = fn
        if cp != -1 and (len(sm) - ss) >= self.min_stable_frames:
            segs.append({'player_id': cp, 'frame_start': ss, 'frame_end': len(sm)-1})
        return segs

    def validate_ball_movement(self, tracks, fs, fe):
        cs = max(0, fs - self.ball_movement_check_radius)
        ce = min(len(tracks['ball']), fe + self.ball_movement_check_radius)
        bp = []
        for f in range(cs, ce):
            bd = tracks['ball'][f].get(1)
            if bd and 'bbox' in bd: bp.append(get_center_of_bbox(bd['bbox']))
        if len(bp) < 2: return 0.0
        dd = measure_distance(bp[0], bp[-1])
        md = max(measure_distance(bp[0], p) for p in bp)
        return max(dd, md)

    def find_player_nearby(self, tracks, pid, tf, sr=None):
        if sr is None: sr = self.player_search_radius
        total = len(tracks['players'])
        pd = tracks['players'][tf].get(pid)
        if pd: return pd, tf
        for off in range(1, sr+1):
            for d in [-off, off]:
                cf = tf + d
                if 0 <= cf < total:
                    pd = tracks['players'][cf].get(pid)
                    if pd: return pd, cf
        return None, -1

    def _get_player_position_for_pass(self, tracks, pid, ft, seg):
        pd, _ = self.find_player_nearby(tracks, pid, ft)
        if pd: return get_center_of_bbox_bottom(pd['bbox'])
        for f in range(seg['frame_start'], min(seg['frame_end']+1, len(tracks['players']))):
            pd = tracks['players'][f].get(pid)
            if pd: return get_center_of_bbox_bottom(pd['bbox'])
        if self._player_identifier:
            j = self._get_jersey(pid)
            if j != "Unknown" and not j.startswith("ID:"):
                for atid in self._player_identifier.get_all_track_ids_for_jersey(j):
                    if atid == pid: continue
                    ad, _ = self.find_player_nearby(tracks, atid, ft)
                    if ad: return get_center_of_bbox_bottom(ad['bbox'])
                    for f in range(seg['frame_start'], min(seg['frame_end']+1, len(tracks['players']))):
                        ad = tracks['players'][f].get(atid)
                        if ad: return get_center_of_bbox_bottom(ad['bbox'])
        return None

    def detect_passes(self, tracks, ball_possessions, player_identifier=None, debug=True):
        if player_identifier: self._player_identifier = player_identifier
        if sum(1 for p in ball_possessions if p != -1) == 0: return []
        if len(set(p for p in ball_possessions if p != -1)) < 2: return []

        filled = self.fill_short_gaps(ball_possessions, max_gap=20)
        filled = self._normalize_possessions_by_jersey(filled)
        smoothed = self.smooth_possessions(filled)
        segments = self.get_stable_segments(smoothed)
        if len(segments) < 2: return []

        merged = [segments[0]]
        for seg in segments[1:]:
            last = merged[-1]
            if seg['player_id'] == last['player_id'] and (seg['frame_start'] - last['frame_end']) <= 10:
                merged[-1]['frame_end'] = seg['frame_end']
            else: merged.append(seg)
        segments = merged

        passes = []; lpf = -999
        for i in range(len(segments)-1):
            sf, st = segments[i], segments[i+1]
            fp, tp = sf['player_id'], st['player_id']
            tfs, tfe = sf['frame_end'], st['frame_start']
            fj, tj = self._get_jersey(fp), self._get_jersey(tp)

            # Filter: skip Unknown / unidentified jerseys, and enforce whitelist if set
            if fj == "Unknown" or fj.startswith("ID:"):
                continue
            if self.allowed_jerseys is not None and fj not in self.allowed_jerseys:
                continue
            if fj == tj:
                if not (fj == "Unknown" and fp != tp): continue
            if (tfe - lpf) < self.cooldown_frames: continue
            if (sf['frame_end'] - sf['frame_start']) < self.min_possession_duration: continue

            from_pos = self._get_player_position_for_pass(tracks, fp, tfs, sf)
            to_pos = self._get_player_position_for_pass(tracks, tp, tfe, st)
            if not from_pos or not to_pos: continue

            dist = measure_distance(from_pos, to_pos)
            if not (self.min_pass_distance <= dist <= self.max_pass_distance): continue

            bm = self.validate_ball_movement(tracks, tfs, tfe)
            if bm < self.ball_movement_threshold: continue

            te = {'frame_start': tfs, 'frame_end': tfe, 'from_pos': from_pos, 'to_pos': to_pos}
            success, reason = self.evaluate_pass_to_target(tracks, te, debug=debug)

            traj = extract_ball_trajectory(tracks, tfs, tfe, buffer_before=self.eval_buffer_before, buffer_after=self.eval_buffer_after)
            cd = float('inf')
            if self._target_cone_pos and traj:
                cd = min(measure_distance(pt, self._target_cone_pos) for pt in traj)

            rs = st['frame_start']
            pdf = min(rs + self.pass_display_delay, st['frame_end'])
            if passes:
                ld = passes[-1]['frame_display']
                if pdf - ld < self.min_display_gap: pdf = ld + self.min_display_gap

            passes.append({
                'frame_start': tfs, 'frame_end': tfe, 'frame_display': pdf,
                'from_player': fp, 'to_player': tp,
                'from_jersey': fj, 'to_jersey': tj,
                'distance': dist, 'ball_movement': bm,
                'success': success, 'target_reason': reason,
                'closest_dist': cd, 'from_pos': from_pos, 'to_pos': to_pos,
            })
            lpf = tfe

        if debug:
            s = sum(1 for p in passes if p['success'])
            g = sum(1 for p in passes if not p['success'])
            pct = s/len(passes)*100 if passes else 0
            print(f"[PASS] Total: {len(passes)}, Sukses: {s}, Gagal: {g}, Akurasi: {pct:.1f}%")
        return passes

    def get_pass_statistics(self, passes):
        total = len(passes)
        sukses = [p for p in passes if p['success']]
        gagal = [p for p in passes if not p['success']]
        pp = {}
        for p in passes:
            j = p['from_jersey']
            if j not in pp: pp[j] = {'total':0,'success':0,'failed':0,'accuracy_pct':0.0,'avg_closest':0.0,'_cs':0.0}
            pp[j]['total'] += 1; pp[j]['_cs'] += p.get('closest_dist', 0.0)
            if p['success']: pp[j]['success'] += 1
            else: pp[j]['failed'] += 1
        for j, s in pp.items():
            s['accuracy_pct'] = round(s['success']/s['total']*100,1) if s['total']>0 else 0.0
            s['avg_closest'] = round(s['_cs']/s['total'],1) if s['total']>0 else 0.0
            del s['_cs']
        return {
            'total_passes': total,
            'successful_passes': len(sukses),
            'failed_passes': len(gagal),
            'accuracy_pct': round(len(sukses)/total*100,1) if total>0 else 0.0,
            'avg_distance': round(float(np.mean([p['distance'] for p in passes])),1) if passes else 0.0,
            'avg_distance_successful': round(float(np.mean([p['distance'] for p in sukses])),1) if sukses else 0.0,
            'avg_closest_dist': round(float(np.mean([p.get('closest_dist',0) for p in passes])),1) if passes else 0.0,
            'per_player': pp
        }
