import os
import json
from pathlib import Path
from datetime import datetime
from typing import Literal, Dict

# Make sure this import path is correct for your project
# You might need to adjust it based on your folder structure and how you run the app.
from generator.image_generator import generate_image 

ASSET_DIR = Path("assets")
OUTPUT_MODEL_DIR = Path("output_model")

def make_dirs():
    # Create required asset and output directories if they don't exist
    for subdir in ["characters", "backgrounds", "rewards", "enemies"]:
        (ASSET_DIR / subdir).mkdir(parents=True, exist_ok=True)
    OUTPUT_MODEL_DIR.mkdir(parents=True, exist_ok=True)


def run_asset_generation(task_id: str, config: dict, jobs_db: Dict):
    """
    This function contains the core logic from your old `generate_assets.py`.
    It's designed to be run in the background.

    :param task_id: The ID of the job we're running.
    :param config: Dictionary with prompts from the frontend.
    :param jobs_db: The shared dictionary to update job status.
    """
    print(f"Starting job {task_id}...")
    jobs_db[task_id]["status"] = "STARTED"
    
    try:
        make_dirs()

        # We will now generate a single config file for this specific run
        # This is useful for `run_game.py` later
        run_config_path = OUTPUT_MODEL_DIR / f"{config['title'].replace(' ', '_')}_config.json"
        with open(run_config_path, 'w') as f:
            json.dump(config, f, indent=4)
        
        # This maps the keys from the frontend to the prompts your generator expects
        prompt_map = {
            "character": config['character'],
            "background": config['background'],
            "reward": config['reward'],
            "enemy": config['enemy'],
        }

        style = "pixel" # You could pass this from the frontend too!
        white_bg = True # For character/enemy sprites

        # Compose prompts
        prompts = {
            "characters": f"{style} sprite of {prompt_map['character']}, 2D side view, {'white background' if white_bg else 'transparent background'}",
            "backgrounds": f"{style} background: {prompt_map['background']}, seamless, game backdrop",
            "rewards": f"{style} icon of {prompt_map['reward']}, 2D, isolated, transparent background",
            "enemies": f"{style} enemy: {prompt_map['enemy']}, 2D side view, pixel art style, {'white background' if white_bg else 'transparent background'}"
        }

        # The result object that the frontend expects
        generated_asset_paths = {
            "title": config['title'],
            "configPath": str(run_config_path) # Path to the specific config for this run
        }

        # Use a timestamp to ensure unique filenames
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        for asset_type, prompt in prompts.items():
            print(f"Generating {asset_type[:-1]} with prompt: {prompt}")
            # The path where the image will be saved (relative to the backend root)
            relative_save_path = Path("assets") / asset_type / f"{asset_type[:-1]}_{timestamp}.png"
            
            # Call your actual image generator
            generate_image(prompt, str(relative_save_path))
            
            # Store the URL-friendly path for the frontend
            # This corresponds to the StaticFiles mount in api.py
            if asset_type == "characters":
                generated_asset_paths["characterUrl"] = str(relative_save_path).replace("\\", "/")
            elif asset_type == "backgrounds":
                generated_asset_paths["backgroundUrl"] = str(relative_save_path).replace("\\", "/")
            elif asset_type == "rewards":
                generated_asset_paths["rewardUrl"] = str(relative_save_path).replace("\\", "/")
            elif asset_type == "enemies":
                generated_asset_paths["enemyUrl"] = str(relative_save_path).replace("\\", "/")

        print(f"Job {task_id} completed successfully.")
        jobs_db[task_id]["status"] = "SUCCESS"
        jobs_db[task_id]["result"] = generated_asset_paths

    except Exception as e:
        print(f"Job {task_id} failed: {e}")
        jobs_db[task_id]["status"] = "FAILURE"
        jobs_db[task_id]["result"] = str(e)