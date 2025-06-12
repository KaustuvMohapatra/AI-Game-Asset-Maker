from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from celery.result import AsyncResult
from tasks import generate_task, celery_app
from schemas import GenerateRequest, JobStatusResponse

app = FastAPI()
app.mount("/output", StaticFiles(directory="output"), name="output")

@app.post("/v1/generate")
def queue_generation(request: GenerateRequest):
    job = generate_task.delay(request.prompt, request.negative_prompt, request.style_id, request.seed)
    return {"job_id": job.id}

@app.get("/v1/jobs/{job_id}", response_model=JobStatusResponse)
def check_status(job_id: str):
    result = AsyncResult(job_id, app=celery_app)
    if result.state == "SUCCESS":
        try:
            result_data = result.result  # ✅ Should be a dict
            return JobStatusResponse(
                job_id=job_id,
                status=result.state,
                result_urls=result_data.get("urls", [])
            )
        except Exception as e:
            return JobStatusResponse(
                job_id=job_id,
                status="ERROR",
                result_urls=[f"Error parsing result: {str(e)}"]
            )
    return JobStatusResponse(job_id=job_id, status=result.state)