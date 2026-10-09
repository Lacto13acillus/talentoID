import os, sys, cv2, pickle, numpy as np
import importlib
from typing import List, Dict, Optional, Any

try:
    YOLO = importlib.import_module("ultralytics").YOLO
except Exception:
    YOLO = None

try:
    sv = importlib.import_module("supervision")
    HAS_SUPERVISION = True
except Exception:
    sv = None
    HAS_SUPERVISION = False



# ============================================================
# CLASS MAPPINGS PER MODEL TYPE
# ============================================================
# Heading model: 0=Heading, 1=ball, 2=player
# Passing model: 0=ball, 1=circle_cone, 2=cone, 3=player

CLASS_MAPS = {
    'heading': {
        'classes': {0: 'heading', 1: 'ball', 2: 'player'},
        'track_keys': ['players', 'ball', 'heading'],
    },
    'passing': {
        'classes': {0: 'ball', 1: 'circle_cone', 2: 'cone', 3: 'player'},
        'track_keys': ['players', 'ball', 'cones'],
    },
}


class Tracker:
    # Legacy constants (heading model) — kept for backward compatibility
    CLASS_HEADING, CLASS_BALL, CLASS_PLAYER = 0, 1, 2
    CLASS_NAMES = {0: 'Heading', 1: 'ball', 2: 'player'}

    def __init__(self, model_path, model_type='heading', conf_threshold=0.25, iou_threshold=0.5):
        """
        Args:
            model_path: path ke model YOLO (.pt)
            model_type: 'heading' atau 'passing' — menentukan class mapping
        """
        global YOLO
        if YOLO is None:
            try:
                YOLO = importlib.import_module("ultralytics").YOLO
            except Exception as e:
                raise ImportError(f"Cannot load YOLO from ultralytics: {e}")
        self.model = YOLO(model_path)
        self.model_type = model_type
        self.conf_threshold = conf_threshold
        self.iou_threshold = iou_threshold

        if HAS_SUPERVISION:
            self.player_tracker = sv.ByteTrack(
                track_activation_threshold=0.25, lost_track_buffer=30,
                minimum_matching_threshold=0.8, frame_rate=30)
            self.heading_tracker = sv.ByteTrack(
                track_activation_threshold=0.25, lost_track_buffer=15,
                minimum_matching_threshold=0.7, frame_rate=30)
            self.cone_tracker = sv.ByteTrack(
                track_activation_threshold=0.25, lost_track_buffer=60,
                minimum_matching_threshold=0.8, frame_rate=30)
        else:
            self.player_tracker = self.heading_tracker = self.cone_tracker = None

        print(f"[TRACKER] Model loaded: {model_path} | type={model_type} | "
              f"ByteTrack: {'Active' if HAS_SUPERVISION else 'Disabled'}")

    @staticmethod
    def read_video(path):
        if not os.path.exists(path): return []
        cap = cv2.VideoCapture(path)
        frames = []
        while True:
            ret, f = cap.read()
            if not ret: break
            frames.append(f)
        cap.release()
        return frames

    @staticmethod
    def save_video(frames, output_path, fps=30, fourcc=None):
        if not frames: return
        h, w = frames[0].shape[:2]
        if fourcc is None:
            ext = os.path.splitext(output_path)[1].lower()
            fourcc = {'mp4':'mp4v', 'avi':'XVID', 'mov':'avc1', 'mkv':'X264'}.get(ext, 'mp4v')
        try: fourcc_code = cv2.VideoWriter_fourcc(*fourcc)
        except: fourcc_code = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_path, fourcc_code, float(fps), (w, h))
        for f in frames: out.write(f.astype(np.uint8))
        out.release()
        print(f"[TRACKER] Saved: {output_path} ({len(frames)}f, {fps}fps, {fourcc})")

    def _detect_frames(self, frames, batch=20):
        detections = []
        for i in range(0, len(frames), batch):
            res = self.model.predict(frames[i:i+batch], conf=self.conf_threshold, iou=self.iou_threshold, verbose=False)
            detections.extend(res)
            if (i//batch)%5==0: print(f"[TRACKER] Detection: {min(i+batch, len(frames))}/{len(frames)}")
        return detections

    # ---------------------------------------------------------
    # HEADING MODEL — detections to tracks (original logic)
    # ---------------------------------------------------------
    def _detections_to_tracks_heading(self, detections):
        tracks = {'players':[], 'ball':[], 'heading':[]}
        for frame_num, det in enumerate(detections):
            boxes = det.boxes
            p_box, p_conf, b_box, b_conf, h_box, h_conf = [], [], [], [], [], []
            for i in range(len(boxes)):
                bbox = boxes.xyxy[i].cpu().numpy().tolist()
                conf = float(boxes.conf[i].cpu().numpy())
                cls = int(boxes.cls[i].cpu().numpy())
                if cls==2: p_box.append(bbox); p_conf.append(conf)
                elif cls==1: b_box.append(bbox); b_conf.append(conf)
                elif cls==0: h_box.append(bbox); h_conf.append(conf)
                
            players = {}
            if p_box:
                if HAS_SUPERVISION and self.player_tracker:
                    sv_det = sv.Detections(xyxy=np.array(p_box), confidence=np.array(p_conf))
                    sv_trk = self.player_tracker.update_with_detections(sv_det)
                    for j in range(len(sv_trk)): players[int(sv_trk.tracker_id[j])] = {'bbox': sv_trk.xyxy[j].tolist()}
                else:
                    for j,b in enumerate(p_box): players[j+1] = {'bbox': b}
            tracks['players'].append(players)
            
            balls = {}
            if b_box: balls[1] = {'bbox': b_box[np.argmax(b_conf)], 'confidence': max(b_conf)}
            tracks['ball'].append(balls)
            
            heads = {}
            if h_box:
                if HAS_SUPERVISION and self.heading_tracker:
                    sv_det = sv.Detections(xyxy=np.array(h_box), confidence=np.array(h_conf))
                    sv_trk = self.heading_tracker.update_with_detections(sv_det)
                    for j in range(len(sv_trk)): heads[int(sv_trk.tracker_id[j])] = {'bbox': sv_trk.xyxy[j].tolist(), 'confidence': float(sv_trk.confidence[j])}
                else:
                    for j,b in enumerate(h_box): heads[j+1] = {'bbox': b, 'confidence': h_conf[j]}
            tracks['heading'].append(heads)
            
            if frame_num%200==0: print(f"[TRACKER] Tracks: {frame_num}/{len(detections)}")
        return tracks

    # ---------------------------------------------------------
    # PASSING MODEL — detections to tracks
    # Class: 0=ball, 1=circle_cone, 2=cone, 3=player
    # Cones (class 1 & 2) are merged into tracks['cones']
    # ---------------------------------------------------------
    def _detections_to_tracks_passing(self, detections):
        tracks = {'players': [], 'ball': [], 'cones': []}
        for frame_num, det in enumerate(detections):
            boxes = det.boxes
            p_box, p_conf = [], []
            b_box, b_conf = [], []
            c_box, c_conf = [], []  # cones (both circle_cone & cone)

            for i in range(len(boxes)):
                bbox = boxes.xyxy[i].cpu().numpy().tolist()
                conf = float(boxes.conf[i].cpu().numpy())
                cls = int(boxes.cls[i].cpu().numpy())
                if cls == 3:    # player
                    p_box.append(bbox); p_conf.append(conf)
                elif cls == 0:  # ball
                    b_box.append(bbox); b_conf.append(conf)
                elif cls in (1, 2):  # circle_cone or cone → merged
                    c_box.append(bbox); c_conf.append(conf)

            # Players with ByteTrack
            players = {}
            if p_box:
                if HAS_SUPERVISION and self.player_tracker:
                    sv_det = sv.Detections(xyxy=np.array(p_box), confidence=np.array(p_conf))
                    sv_trk = self.player_tracker.update_with_detections(sv_det)
                    for j in range(len(sv_trk)):
                        players[int(sv_trk.tracker_id[j])] = {'bbox': sv_trk.xyxy[j].tolist()}
                else:
                    for j, b in enumerate(p_box):
                        players[j+1] = {'bbox': b}
            tracks['players'].append(players)

            # Ball (highest confidence)
            balls = {}
            if b_box:
                balls[1] = {'bbox': b_box[np.argmax(b_conf)], 'confidence': max(b_conf)}
            tracks['ball'].append(balls)

            # Cones with ByteTrack (stable IDs penting untuk gate detection)
            cones = {}
            if c_box:
                if HAS_SUPERVISION and self.cone_tracker:
                    sv_det = sv.Detections(xyxy=np.array(c_box), confidence=np.array(c_conf))
                    sv_trk = self.cone_tracker.update_with_detections(sv_det)
                    for j in range(len(sv_trk)):
                        cones[int(sv_trk.tracker_id[j])] = {
                            'bbox': sv_trk.xyxy[j].tolist(),
                            'confidence': float(sv_trk.confidence[j])
                        }
                else:
                    for j, b in enumerate(c_box):
                        cones[j+1] = {'bbox': b, 'confidence': c_conf[j]}
            tracks['cones'].append(cones)

            if frame_num % 200 == 0:
                print(f"[TRACKER] Tracks: {frame_num}/{len(detections)}")
        return tracks

    # ---------------------------------------------------------
    # Router — pilih method berdasarkan model_type
    # ---------------------------------------------------------
    def _detections_to_tracks(self, detections):
        if self.model_type == 'passing':
            return self._detections_to_tracks_passing(detections)
        else:
            return self._detections_to_tracks_heading(detections)

    def _interpolate_ball_positions(self, tracks, max_gap=15):
        frames = tracks['ball']
        det = [i for i,f in enumerate(frames) if f.get(1) and 'bbox' in f[1]]
        if len(det)<2: return tracks
        for idx in range(len(det)-1):
            s, e = det[idx], det[idx+1]
            gap = e-s-1
            if gap<=0 or gap>max_gap: continue
            sb, eb = frames[s][1]['bbox'], frames[e][1]['bbox']
            for g in range(1, gap+1):
                t = g/(gap+1)
                frames[s+g][1] = {'bbox': [sb[j]+(eb[j]-sb[j])*t for j in range(4)], 'confidence':0.0, 'interpolated':True}
        return tracks

    def get_object_tracks(self, frames, read_from_stub=False, stub_path="stubs/tracks.pkl", interpolate_ball=True, ball_interpolation_max_gap=15):
        if read_from_stub and os.path.exists(stub_path):
            with open(stub_path, 'rb') as f: tracks = pickle.load(f)
            # Ensure all expected keys exist
            if self.model_type == 'heading' and 'heading' not in tracks:
                tracks['heading'] = [{} for _ in range(len(frames))]
            if self.model_type == 'passing' and 'cones' not in tracks:
                tracks['cones'] = [{} for _ in range(len(frames))]
            return tracks
        det = self._detect_frames(frames)
        tracks = self._detections_to_tracks(det)
        if interpolate_ball: tracks = self._interpolate_ball_positions(tracks, ball_interpolation_max_gap)
        os.makedirs(os.path.dirname(stub_path), exist_ok=True)
        with open(stub_path, 'wb') as f: pickle.dump(tracks, f)
        return tracks