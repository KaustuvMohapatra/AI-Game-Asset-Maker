import os
import json
from PIL import Image
from transformers import pipeline
from diffusers import StableDiffusionPipeline
import torch

# Initialize caption generator (BLIP)
captioner = pipeline("image-to-text", model="Salesforce/blip-image-captioning-base")

# Initialize Stable Diffusion image generation pipeline
pipe = StableDiffusionPipeline.from_pretrained(
    "CompVis/stable-diffusion-v1-4",
    torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
    variant="fp16" if torch.cuda.is_available() else None,
).to("cuda" if torch.cuda.is_available() else "cpu")

def generate_creature_with_caption(prompt, filename):
    # Generate image
    image = pipe(prompt).images[0]
    image.save(filename)

    # Generate caption
    caption = captioner(filename)[0]['generated_text']

    return {
        "image": f"./outputs/{os.path.basename(filename)}",
        "text": caption,
        "prompt": prompt
    }

def load_prompts(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]

def main():
    os.makedirs("outputss", exist_ok=True)

    # Creature prompt themes
    themes = load_prompts("C:/nus_adv/fantasy_creature_prompts.txt")

    dataset = []
    for i, theme in enumerate(themes):
        prompt = f"{theme}, 2D stylized realism, game creature, isolated on white background"
        filename = os.path.join("outputs", f"creature_{i}.png")
        result = generate_creature_with_caption(prompt, filename)
        dataset.append(result)
        print(f"[{i+1}] Generated: {result['text']}")

    # Save metadata JSON
    with open("outputs/game_creatures.json", "w", encoding="utf-8") as f:
        json.dump(dataset, f, indent=2)

    print("\nDataset saved with", len(dataset), "entries in the 'outputs' folder.")
    print("Files in outputs:", os.listdir("outputs"))

if __name__ == "__main__":
    main()
