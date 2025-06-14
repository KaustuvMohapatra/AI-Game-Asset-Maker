# generator/image_generator.py

from diffusers import StableDiffusionPipeline
import torch
from PIL import Image

# Load pipeline globally once to avoid slow repeat loads
pipe = StableDiffusionPipeline.from_pretrained(
    "stabilityai/stable-diffusion-2-1",
    torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32
)
pipe = pipe.to("cuda" if torch.cuda.is_available() else "cpu")

def generate_image(prompt: str, output_path: str):
    """
    Generate an image from text prompt using Stable Diffusion 2.1.
    Save result to the given output path.
    """
    print(f"Prompt: {prompt}")
    
    image: Image.Image = pipe(prompt, guidance_scale=7.5).images[0]
    image.save(output_path)
    print(f"Saved: {output_path}")