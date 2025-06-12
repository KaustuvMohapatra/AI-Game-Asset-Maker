# tasks.py
from celery import Celery
from pathlib import Path
import random

celery_app = Celery(
    "game_asset_worker",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)

celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
)

@celery_app.task(name="generate_task")
def generate_task(prompt, negative_prompt, style_id, seed):
    from diffusers import StableDiffusionPipeline
    import torch

    pipe = StableDiffusionPipeline.from_pretrained(
        "stabilityai/stable-diffusion-2-1",
        torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32
    )

    device = "cuda" if torch.cuda.is_available() else "cpu"
    pipe.to(device)

    if seed < 0:
        seed = random.randint(0, 2**32 - 1)

    generator = torch.Generator(device=device).manual_seed(seed)
    image = pipe(prompt=prompt, negative_prompt=negative_prompt, generator=generator).images[0]

    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    filename = f"{style_id}_{seed}.png"
    image_path = output_dir / filename
    image.save(image_path)

    return {"urls": [f"/output/{filename}"]}