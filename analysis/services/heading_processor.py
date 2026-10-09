import os
import sys
import cv2
import logging
import numpy as np
from typing import Dict, List, Optional, Any, Tuple

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if PROJECT_ROOT not in sys.path: sys.path.insert(0, PROJECT_ROOT)

from analysis.trackers.tracker import Tracker
from analysis.trackers.heading_detector import HeadingDetector
from analysis.utils.draw_headings import (
    draw_head_bbox_on_frame, draw_heading_status, draw_heading_result_flash,
    draw_heading_stats_panel, draw_ball_trajectory_on_frame
)
from analysis.utils.bbox_utils import get_center_of_bbox

logger = logging.getLogger(__name__)

def run_heading_pipeline(input_path, output_path, job_id, model_path, fps=30, 
                         use_stub=False, stub_path=None, config_overrides=None):
    result = {'job_id': job_id, 'status': 'processing', 'progress': 0,
              'stats': None, 'heading_events': [], 'output_video': None, 'error': None}
    
    cfg = {
        "head_bbox_margin": 20.0, "max_head_ball_center_distance": 80.0,
        "max_approach_distance": 200.0, "min_approach_frames": 2,
        "cooldown_frames": 25, "max_approach_duration_sec": 4.0,
        "min_away_frames": 5, "show_head_bbox": True, "show_stats_panel": True,
        "debug_trajectory": False, "show_heading_status": True,
        "result_flash_frames": 45, "output_format": "mp4",
        **(config_overrides or {})
    }

    try:
        logger.info(f"[{job_id}] Reading video: {input_path}")
        frames = Tracker.read_video(input_path)
        if not frames: raise ValueError("Video empty")
        result['progress'] = 10

        logger.info(f"[{job_id}] Running tracking...")
        tracker = Tracker(model_path=model_path)
        if not stub_path:
            stub_path = os.path.join(PROJECT_ROOT, 'static', 'stubs', f"{job_id}_tracks.pkl")
            os.makedirs(os.path.dirname(stub_path), exist_ok=True)
            
        tracks = tracker.get_object_tracks(frames, read_from_stub=use_stub, stub_path=stub_path)
        if 'heading' not in tracks: tracks['heading'] = [{} for _ in range(len(frames))]
        result['progress'] = 40

        logger.info(f"[{job_id}] Detecting headings...")
        detector = HeadingDetector(fps=fps)
        for k, v in cfg.items():
            if hasattr(detector, k): setattr(detector, k, v)
            
        events = detector.detect_headings(tracks, debug=False)
        stats = detector.get_heading_statistics(events)
        result['stats'] = stats
        result['heading_events'] = events
        result['progress'] = 70

        logger.info(f"[{job_id}] Rendering video...")
        out_frames = _render_frames(frames, tracks, events, detector, cfg)
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        fourcc = 'mp4v' if cfg.get('output_format') == 'mp4' else 'XVID'
        Tracker.save_video(out_frames, output_path, fps=fps, fourcc=fourcc)
        
        result['output_video'] = output_path
        result['progress'] = 100
        result['status'] = 'completed'
        logger.info(f"[{job_id}] Done. {stats['total_headings']} headings.")
        
    except Exception as e:
        logger.error(f"[{job_id}] Failed: {str(e)}", exc_info=True)
        result['status'] = 'failed'
        result['error'] = str(e)
        
    return result

def _render_frames(frames, tracks, events, detector, config):
    output_frames, total = [], len(frames)
    trajectory = []
    event_map = {f: e for e in events for f in range(e['frame_start'], e['frame_end']+1)}
    flash_map = {}
    for e in events:
        dur = config.get("result_flash_frames", 45)
        for f in range(e['frame_end'], min(e['frame_end']+dur, total)):
            flash_map[f] = {'event': e, 'progress': 1.0 - (f - e['frame_end'])/dur}

    for i, frame in enumerate(frames):
        out = frame.copy()
        evt = event_map.get(i)
        flash = flash_map.get(i)

        for pid, pd in tracks["players"][i].items():
            bbox = pd.get("bbox")
            if not bbox: continue
            x1,y1,x2,y2 = map(int, bbox)
            c = (0,200,50) if evt and evt.get('player_id')==pid else (200,80,50)
            cv2.rectangle(out, (x1,y1), (x2,y2), c, 2)

        if config.get("show_head_bbox"):
            for hd in tracks.get('heading', [{}]*total)[i].values():
                hb = hd.get('bbox')
                if not hb: continue
                sc, sf, sl = False, False, False
                if flash: sf, sl = flash['event']['success'], not flash['event']['success']
                elif evt: sc = True
                out = draw_head_bbox_on_frame(out, hb, sc, sf, sl)

        bd = tracks["ball"][i].get(1)
        if bd and 'bbox' in bd:
            bx1,by1,bx2,by2 = map(int, bd["bbox"])
            cx,cy,r = (bx1+bx2)//2, (by1+by2)//2, max(8,(bx2-bx1)//2)
            cv2.circle(out, (cx,cy), r, (0,230,255), 2)
            if config.get("debug_trajectory"):
                trajectory.append((cx,cy))
                if len(trajectory)>60: trajectory.pop(0)

        if config.get("debug_trajectory") and len(trajectory)>1:
            out = draw_ball_trajectory_on_frame(out, trajectory, 40)

        if config.get("show_heading_status") and evt:
            out = draw_heading_status(out, True, evt['frame_contact']==i,
                                      evt.get('player_id',-1), evt.get('head_ball_distance',0), evt.get('iou',0))

        if flash:
            e = flash['event']
            out = draw_heading_result_flash(out, e['success'], e['event_id'],
                                            e['head_ball_distance'], e.get('iou',0), flash['progress'])

        if config.get("show_stats_panel"):
            so_far = [ev for ev in events if ev['frame_end']<=i]
            s = sum(1 for ev in so_far if ev['success'])
            t = len(so_far)
            stats = {'total_headings':t, 'successful_headings':s, 'failed_headings':t-s,
                     'accuracy_pct':round(s/t*100,1) if t>0 else 0.0}
            out = draw_heading_stats_panel(out, stats, (20,20), 280)

        h,w = out.shape[:2]
        cv2.putText(out, f"Frame: {i}", (w-140, h-10), cv2.FONT_HERSHEY_SIMPLEX, 0.42, (110,110,110), 1)
        output_frames.append(out)
    return output_frames