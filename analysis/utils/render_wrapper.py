from analysis.services.heading_processor import _render_frames


def render_frames_wrapper(frames, tracks, heading_events, heading_detector, config):
    """Wrapper to render output frames using heading_processor's renderer."""
    return _render_frames(
        frames=frames,
        tracks=tracks,
        events=heading_events,
        detector=heading_detector,
        config=config,
    )
