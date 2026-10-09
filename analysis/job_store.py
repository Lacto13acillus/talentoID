import uuid
from typing import Dict, Optional


class JobStore:
    """In-memory job store — port dari Flask JobStore."""
    _jobs: Dict[str, Dict] = {}

    @classmethod
    def init(cls):
        cls._jobs.clear()

    @classmethod
    def create_job(cls, mode: str, input_path: str, original_filename: str) -> str:
        job_id = str(uuid.uuid4())[:8]
        cls._jobs[job_id] = {
            "job_id": job_id,
            "mode": mode,
            "status": "pending",
            "progress": 0,
            "input_path": input_path,
            "original_filename": original_filename,
            "output_video": None,
            "stats": None,
            "events": None,
            "error": None,
        }
        return job_id

    @classmethod
    def get_job(cls, job_id: str) -> Optional[Dict]:
        return cls._jobs.get(job_id)

    @classmethod
    def update_job(cls, job_id: str, data: Dict):
        if job_id in cls._jobs:
            cls._jobs[job_id].update(data)

    # Alias compatibility
    create = create_job
    get = get_job
    update = update_job
