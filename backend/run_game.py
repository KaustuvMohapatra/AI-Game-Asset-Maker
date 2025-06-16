import pygame
import json
import os
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
pygame.display.set_caption("Generative Game")
clock = pygame.time.Clock()

# Load config
with open("config/game_config.json") as f:
    config = json.load(f)

# Load image utilities
def load_latest_image(folder):
    files = sorted(os.listdir(folder), reverse=True)
    if not files:
        raise Exception(f"No images found in {folder}")
    return load_image_make_transparent(os.path.join(folder, files[0]))

def load_image_make_transparent(path, colorkey=(255, 255, 255)):
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

# Load background image and assets
bg_folder = "assets/backgrounds"
bg_image_file = sorted(os.listdir(bg_folder), reverse=True)[0]
bg_image_path = os.path.join(bg_folder, bg_image_file)

BG_IMG = pygame.transform.scale(load_image_make_transparent(bg_image_path), (WIDTH, HEIGHT))
platform_color = darken_color(get_average_color(bg_image_path))

CHAR_IMG = pygame.transform.scale(load_latest_image("assets/characters"), (64, 64))
ENEMY_IMG = pygame.transform.scale(load_latest_image("assets/enemies"), (64, 64))
REWARD_IMG = pygame.transform.scale(load_latest_image("assets/rewards"), (32, 32))

# Game entities
player = Player(100, HEIGHT - 40, CHAR_IMG)  # Positioned a bit above lowest platform (40px platform height + 40px offset)
reward_rect = pygame.Rect(WIDTH + 200, HEIGHT - 90, 32, 32)

# Create enemies on each platform
enemies = [
    Enemy(WIDTH + 100, HEIGHT - 100, ENEMY_IMG),       # Ground enemy
    Enemy(400 + 50, 400 - 64, ENEMY_IMG),              # On 2nd platform
    Enemy(700 + 50, 300 - 64, ENEMY_IMG),              # On 3rd platform
    Enemy(1000 + 50, 350 - 64, ENEMY_IMG),             # On 4th platform
]

score = 0

# Background scroller
bg_scroller = BackgroundScroller(BG_IMG, speed=3)

# Platforms with color matched to background
platforms = [
    Platform(0, HEIGHT - 40, WIDTH * 2, 40, color=platform_color),
    Platform(400, 400, 120, 20, color=platform_color),
    Platform(700, 300, 100, 20, color=platform_color),
    Platform(1000, 350, 150, 20, color=platform_color),
]

# Font
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

        # Input & update player with platform collision
        player.handle_keys()
        player.update(platforms)

        # Scroll enemies, reward, and platforms with background
        for enemy in enemies:
            enemy.rect.x -= bg_scroller.speed
            if enemy.rect.right < 0:
                enemy.rect.left = WIDTH + 100
        reward_rect.x -= bg_scroller.speed
        if reward_rect.right < 0:
            reward_rect.left = WIDTH + 300
        for plat in platforms:
            plat.move(bg_scroller.speed)

        # Check collisions
        for enemy in enemies:
            enemy.check_collision_and_damage(player)
        if player.rect.colliderect(reward_rect):
            score += 1
            reward_rect.left = WIDTH + 300

        # Draw all
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

if __name__ == "__main__":
    main()
