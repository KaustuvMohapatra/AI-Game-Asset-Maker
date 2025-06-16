import json
import os

CONFIG_PATH = "config/game_config.json"

def get_user_input():
    print("=" * 60)
    print("Welcome to the Side-Scrolling Generative Game Builder")
    print("=" * 60)

    title = input("\nEnter your game's title: ").strip()
    if not title:
        title = "Untitled Side-Scroller"

    print("\nDescribe your game assets:")
    
    character = input("Main character (left-side jumper only, e.g., 'pixel knight', 'robot cat'): ").strip()
    if not character:
        character = "pixel knight"

    background = input("Background (will scroll left, e.g., 'enchanted forest', 'cyberpunk city'): ").strip()
    if not background:
        background = "enchanted forest"

    reward = input("Reward item (e.g., 'floating crystal', 'gold coin'): ").strip()
    if not reward:
        reward = "gold coin"

    enemy = input("Enemy (moves toward player, e.g., 'slime monster', 'flying drone'): ").strip()
    if not enemy:
        enemy = "slime monster"

    num_levels = input("How many levels should the game have? (default = 3): ").strip()
    num_levels = int(num_levels) if num_levels.isdigit() else 3

    config = {
        "title": title,
        "character_prompt": character,
        "background_prompt": background,
        "reward_prompt": reward,
        "enemy_prompt": enemy,
        "levels": num_levels
    }

    os.makedirs("config", exist_ok=True)
    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f, indent=4)

    print(f"\nConfiguration saved to `{CONFIG_PATH}`")
    print("You're now ready to run `generate_assets.py` to generate game art!")

    return config


if __name__ == "__main__":
    get_user_input()
