import json
import os
from pathlib import Path
from datetime import datetime
from typing import Literal

# === Replace this with your actual image generation function ===
from generator.image_generator import generate_image  # <- this must call your backend

CONFIG_PATH = "config/game_config.json"
ASSET_DIR = Path("assets")

def make_dirs():
    for subdir in ["characters", "backgrounds", "rewards", "enemies"]:
        (ASSET_DIR / subdir).mkdir(parents=True, exist_ok=True)

def generate_assets(config: dict, style: Literal["pixel", "realistic", "cartoon"] = "pixel"):
    print("Generating assets using Stable Diffusion...\n")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    prompts = {
        "character": f"{style} sprite of {config['character_prompt']}, 2D side view, transparent background",
        "background": f"{style} background: {config['background_prompt']}, seamless, game backdrop",
        "reward": f"{style} icon of {config['reward_prompt']}, 2D, isolated, transparent background",
        "enemy": f"{style} enemy: {config['enemy_prompt']}, 2D side view, pixel art style"
    }

    outputs = {
        "character": ASSET_DIR / "characters" / f"character_{timestamp}.png",
        "background": ASSET_DIR / "backgrounds" / f"background_{timestamp}.png",
        "reward": ASSET_DIR / "rewards" / f"reward_{timestamp}.png",
        "enemy": ASSET_DIR / "enemies" / f"enemy_{timestamp}.png"
    }

    for key in prompts:
        print(f"Generating {key}...")
        generate_image(prompts[key], str(outputs[key]))  # Custom backend call

    print("\nAll assets generated and saved under /assets/")

def load_config():
    with open(CONFIG_PATH, "r") as f:
        return json.load(f)

if __name__ == "__main__":
    make_dirs()
    config = load_config()
    generate_assets(config)