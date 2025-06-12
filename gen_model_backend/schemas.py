from pydantic import BaseModel
from typing import Optional, List

class GenerateRequest(BaseModel):
    prompt: str
    negative_prompt: Optional[str] = ""
    style_id: str
    seed: int = -1

class JobStatusResponse(BaseModel):
    job_id: str
    status: str
    result_urls: Optional[List[str]] = None