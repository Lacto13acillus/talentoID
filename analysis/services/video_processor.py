# app/services/video_processor.py
import os
import sys
import logging
from typing import Dict, Optional
import cv2
import numpy as np

# Tambahkan path ke trackers & utils project asli
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from analysis.trackers.tracker import Tracker
from analysis.trackers.heading_detector import HeadingDetector

logger = logging.getLogger(__name__)

class VideoProcessor:
    """Wrapper untuk pipeline heading detection yang sudah ada."""
    
    def __init__(self, config: Dict):
        self.config = config
        self.model_path = config['model_path']
        self.fps = config.get('fps', 30)
        
        # Parameter heading detector
        self.heading_params = {
            'head_bbox_margin': config.get('head_bbox_margin', 20.0),
            'max_head_ball_center_distance': config.get('max_head_ball_center_distance', 80.0),
            'max_approach_distance': config.get('max_approach_distance', 200.0),
            'min_approach_frames': config.get('min_approach_frames', 2),
            'cooldown_frames': config.get('cooldown_frames', 25),
            'max_approach_duration_sec': config.get('max_approach_duration_sec', 4.0),
            'min_away_frames': config.get('min_away_frames', 5),
        }
    
    def process(self, 
                input_path: str, 
                output_path: str,
                job_id: str,
                use_stub: bool = False,
                stub_path: Optional[str] = None) -> Dict:
        """
        Jalankan pipeline heading detection.
        
        Returns:
            Dict dengan status, stats, dan paths.
        """
        result = {
            'job_id': job_id,
            'status': 'processing',
            'progress': 0,
            'stats': None,
            'output_video': None,
            'error': None
        }
        
        try:
            # === TAHAP 1: Baca Video ===
            logger.info(f"[{job_id}] Membaca video: {input_path}")
            frames = Tracker.read_video(input_path)
            if not frames:
                raise ValueError("Video kosong atau tidak bisa dibaca")
            
            result['progress'] = 10
            total_frames = len(frames)
            
            # === TAHAP 2: Deteksi & Tracking ===
            logger.info(f"[{job_id}] Menjalankan tracking...")
            tracker = Tracker(model_path=self.model_path)
            
            tracks = tracker.get_object_tracks(
                frames,
                read_from_stub=use_stub,
                stub_path=stub_path or os.path.join(
                    self.config['stubs_folder'], f"{job_id}_tracks.pkl"
                )
            )
            
            # Pastikan key 'heading' ada
            if 'heading' not in tracks:
                tracks['heading'] = [{} for _ in range(total_frames)]
            
            result['progress'] = 50
            
            # === TAHAP 3: Heading Detection ===
            logger.info(f"[{job_id}] Mendeteksi heading events...")
            heading_detector = HeadingDetector(fps=self.fps)
            
            # Apply parameters
            for key, value in self.heading_params.items():
                setattr(heading_detector, key, value)
            
            heading_events = heading_detector.detect_headings(tracks, debug=False)
            stats = heading_detector.get_heading_statistics(heading_events)
            
            result['progress'] = 80
            
            # === TAHAP 4: Render Output Video ===
            logger.info(f"[{job_id}] Merender video output...")
            
            from analysis.utils.render_wrapper import render_frames_wrapper
            output_frames = render_frames_wrapper(
                frames=frames,
                tracks=tracks,
                heading_events=heading_events,
                heading_detector=heading_detector,
                config=self.config
            )
            
            # Simpan video
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            Tracker.save_video(output_frames, output_path, fps=self.fps)
            
            result['progress'] = 100
            result['status'] = 'completed'
            result['stats'] = stats
            result['output_video'] = output_path
            result['heading_events'] = heading_events  # Optional: return detail events
            
            logger.info(f"[{job_id}] ✅ Processing selesai: {stats['total_headings']} heading terdeteksi")
            
        except Exception as e:
            logger.error(f"[{job_id}] ❌ Error: {str(e)}", exc_info=True)
            result['status'] = 'failed'
            result['error'] = str(e)
        
        return result