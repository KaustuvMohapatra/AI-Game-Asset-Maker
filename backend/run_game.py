import pygame
import json
import os
import sys  # <-- ADDED: To read command-line arguments
from PIL import Image
import numpy as np

from engine.player import Player
from engine.enemy import Enemy
from engine.platform import Platform
from engine.level import BackgroundScroller, draw_score

# Initialize Pygame
pygame.init()
WIDTH, HEIGHT = 960, 540
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()


# --- SECTION 1: UPDATED CONFIGURATION LOADER ---
# This block replaces the old hardcoded path. It now accepts a path from the command line,
# which is how your Electron app will tell the game which configuration to run.

if len(sys.argv) > 1:
    # If a command-line argument is provided, use it as the path
    config_path = sys.argv[1]
    print(f"Loading configuration from provided path: {config_path}")
else:
    # This is a fallback for when you run the script directly for testing
    print("Usage: python run_game.py <path_to_config_json>")
    output_dir = "output_model"
    
    if not os.path.exists(output_dir):
        raise FileNotFoundError(f"ERROR: The fallback directory '{output_dir}' was not found. Please generate assets first.")

    # Find the most recently modified .json file in the output_model directory
    configs = sorted(
        [os.path.join(output_dir, f) for f in os.listdir(output_dir) if f.endswith('.json')],
        key=os.path.getmtime,
        reverse=True
    )
    if not configs:
        raise Exception("No config file provided and none found in output_model.")
    config_path = configs[0]
    print(f"No config path provided, using latest found: {config_path}")

try:
    with open(config_path) as f:
        config = json.load(f)
except FileNotFoundError:
    print(f"FATAL ERROR: The configuration file was not found at the path: {config_path}")
    pygame.quit()
    sys.exit() # Exit the script if the config can't be found

# Set the window title from the loaded configuration
pygame.display.set_caption(config.get("title", "Generative Game"))


# --- SECTION 2: UPDATED IMAGE LOADING UTILITIES ---

def load_latest_image(folder):
    """
    Finds the most recently modified image in a folder and returns it as a transparent Surface.
    This is more reliable than sorting by name.
    """
    if not os.path.exists(folder):
        raise FileNotFoundError(f"Asset folder not found: {folder}")
        
    files = sorted(
        [os.path.join(folder, f) for f in os.listdir(folder) if f.endswith(('.png', '.jpg', '.jpeg'))],
        key=os.path.getmtime,
        reverse=True
    )
    if not files:
        raise Exception(f"No images found in {folder}")
    
    latest_file = files[0]
    print(f"Loading latest image from '{folder}': {os.path.basename(latest_file)}")
    return load_image_make_transparent(latest_file)

def load_image_make_transparent(path, colorkey=(255, 255, 255)):
    """Loads an image and sets its white background to be transparent."""
    image = pygame.image.load(path).convert()
    image.set_colorkey(colorkey)
    return image.convert_alpha()

# Utility: get average color from background image (PIL + numpy)
def get_average_color(image_path):
    img = Image.open(image_path).convert('RGB')
    img_np = np.array(img)
    avg_color = img_np.mean(axis=(0,1)).astype(int)
    return tuple(avg_color)

# Darken color for better platform visibility
def darken_color(color, amount=40):
    return tuple(max(c - amount, 0) for c in color)


# --- SECTION 3: ASSET LOADING (No changes needed, but now uses the updated functions) ---

# Find the absolute path of the latest background image to use for color averaging
bg_folder = "assets/backgrounds"
latest_bg_path = sorted([os.path.join(bg_folder, f) for f in os.listdir(bg_folder)], key=os.path.getmtime, reverse=True)[0]

BG_IMG = pygame.transform.scale(load_image_make_transparent(latest_bg_path), (WIDTH, HEIGHT))
platform_color = darken_color(get_average_color(latest_bg_path))

CHAR_IMG = pygame.transform.scale(load_latest_image("assets/characters"), (64, 64))
ENEMY_IMG = pygame.transform.scale(load_latest_image("assets/enemies"), (64, 64))
REWARD_IMG = pygame.transform.scale(load_latest_image("assets/rewards"), (32, 32))


# --- ALL REMAINING GAME LOGIC IS UNCHANGED ---

# Game entities
player = Player(100, HEIGHT - 80, CHAR_IMG)
reward_rect = pygame.Rect(WIDTH + 200, HEIGHT - 90, 32, 32)

# Create enemies on each platform
enemies = [
    Enemy(WIDTH + 100, HEIGHT - 100, ENEMY_IMG),
    Enemy(400 + 50, 400 - 64, ENEMY_IMG),
    Enemy(700 + 50, 300 - 64, ENEMY_IMG),
    Enemy(1000 + 50, 350 - 64, ENEMY_IMG),
]

score = 0
bg_scroller = BackgroundScroller(BG_IMG, speed=3)
platforms = [
    Platform(0, HEIGHT - 40, WIDTH * 2, 40, color=platform_color),
    Platform(400, 400, 120, 20, color=platform_color),
    Platform(700, 300, 100, 20, color=platform_color),
    Platform(1000, 350, 150, 20, color=platform_color),
]
font = pygame.font.SysFont(None, 28)

def draw_hud():
    draw_score(screen, score, player.health)

def main():
    global score
    running = True

    while running:
        clock.tick(60)
        screen.fill((0, 0, 0))
        bg_scroller.update()
        bg_scroller.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        player.handle_keys()
        player.update(platforms)

        for enemy in enemies:
            enemy.rect.x -= bg_scroller.speed
            if enemy.rect.right < 0:
                enemy.rect.left = WIDTH + 100
        reward_rect.x -= bg_scroller.speed
        if reward_rect.right < 0:
            reward_rect.left = WIDTH + 300
        for plat in platforms:
            plat.move(bg_scroller.speed)

        for enemy in enemies:
            enemy.check_collision_and_damage(player)
        if player.rect.colliderect(reward_rect):
            score += 1
            reward_rect.left = WIDTH + 300

        for plat in platforms:
            plat.draw(screen)

        player.draw(screen)
        for enemy in enemies:
            enemy.draw(screen)
        screen.blit(REWARD_IMG, reward_rect)
        draw_hud()

        if not player.is_alive():
            print("Game Over!")
            running = False

        pygame.display.update()

    pygame.quit()
    sys.exit() # Ensure the script fully closes

if __name__ == "__main__":
    main()