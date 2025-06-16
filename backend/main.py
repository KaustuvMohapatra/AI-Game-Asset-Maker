import json
import os

CONFIG_PATH = "config/game_config.json"

def get_user_input():
    print("Welcome to the Generative AI Game Builder\n")
    
    title = input("Enter your game's title: ")
    
    character = input("Describe your main character (e.g., 'ninja cat', 'pixel knight'): ")
    background = input("Describe the game's background (e.g., 'space station', 'ancient jungle'): ")
    reward = input("Describe the in-game reward items (e.g., 'gold coins', 'magic scrolls'): ")
    
    num_levels = input("How many levels should the game have? (default: 3): ")
    num_levels = int(num_levels.strip()) if num_levels.strip().isdigit() else 3

    enemy = input("Describe the enemy type (e.g., 'robots', 'zombies'): ")
    
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
    
    print(f"\nConfiguration saved to {CONFIG_PATH}. You're ready to generate assets!")
    return config


if __name__ == "__main__":
    get_user_input()