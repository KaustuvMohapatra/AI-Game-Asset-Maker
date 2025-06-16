import json
import os
from pathlib import Path
from datetime import datetime
from typing import Literal

# Replace this with your actual image generation function import
from generator.image_generator import generate_image  # Must call your backend


CONFIG_PATH = Path("config/game_config.json")
ASSET_DIR = Path("assets")


def make_dirs():
    # Create required asset subdirectories if they don't exist
    for subdir in ["characters", "backgrounds", "rewards", "enemies"]:
        (ASSET_DIR / subdir).mkdir(parents=True, exist_ok=True)


def generate_assets(config: dict, style: Literal["pixel", "realistic", "cartoon"] = "pixel", white_bg=False):
    """
    Generate game assets using a generative model backend.

    :param config: Dictionary with prompts for each asset type
    :param style: Art style to apply (pixel, realistic, cartoon)
    :param white_bg: If True, force white background in prompts (for characters and enemies)
    """
    print("Generating assets using Stable Diffusion...\n")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Compose prompts with optional white background
    character_bg_prompt = "white background" if white_bg else "transparent background"
    enemy_bg_prompt = "white background" if white_bg else "transparent background"

    prompts = {
        "characters": f"{style} sprite of {config['character_prompt']}, 2D side view, {character_bg_prompt}",
        "backgrounds": f"{style} background: {config['background_prompt']}, seamless, game backdrop",
        "rewards": f"{style} icon of {config['reward_prompt']}, 2D, isolated, transparent background",
        "enemies": f"{style} enemy: {config['enemy_prompt']}, 2D side view, pixel art style, {enemy_bg_prompt}"
    }

    outputs = {
        "characters": ASSET_DIR / "characters" / f"character_{timestamp}.png",
        "backgrounds": ASSET_DIR / "backgrounds" / f"background_{timestamp}.png",
        "rewards": ASSET_DIR / "rewards" / f"reward_{timestamp}.png",
        "enemies": ASSET_DIR / "enemies" / f"enemy_{timestamp}.png"
    }

    for asset_type, prompt in prompts.items():
        print(f"Generating {asset_type[:-1]}...")
        generate_image(prompt, str(outputs[asset_type]))

    print("\nAll assets generated and saved under /assets/")


def load_config():
    with open(CONFIG_PATH, "r") as f:
        return json.load(f)


if __name__ == "__main__":
    make_dirs()
    config = load_config()
    generate_assets(config, style="pixel", white_bg=True)  # Set white_bg=True to force white backgrounds
