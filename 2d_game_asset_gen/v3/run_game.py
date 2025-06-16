import pygame
import json
import os
from engine.player import Player
from engine.enemy import Enemy
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

# Utility to load image with transparency
def load_latest_image(folder):
    files = sorted(os.listdir(folder), reverse=True)
    if not files:
        raise Exception(f"No images found in {folder}")
    return load_image_make_transparent(os.path.join(folder, files[0]))

def load_image_make_transparent(path, colorkey=(255, 255, 255)):
    image = pygame.image.load(path).convert()
    image.set_colorkey(colorkey)
    return image.convert_alpha()

# Load assets
CHAR_IMG = pygame.transform.scale(load_latest_image("assets/characters"), (64, 64))
BG_IMG = pygame.transform.scale(load_latest_image("assets/backgrounds"), (960, 540))
ENEMY_IMG = pygame.transform.scale(load_latest_image("assets/enemies"), (64, 64))
REWARD_IMG = pygame.transform.scale(load_latest_image("assets/rewards"), (32, 32))

# Initialize game entities
player = Player(100, HEIGHT - 100, CHAR_IMG)
enemy = Enemy(WIDTH, HEIGHT - 100, ENEMY_IMG)
reward_rect = pygame.Rect(WIDTH + 200, HEIGHT - 90, 32, 32)
score = 0

# Background scroller
bg_scroller = BackgroundScroller(BG_IMG, speed=3)

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

        # Player logic
        player.handle_keys()
        player.update()

        # Move enemy and reward with background
        enemy.rect.x -= bg_scroller.speed
        if enemy.rect.right < 0:
            enemy.rect.left = WIDTH + 100

        reward_rect.x -= bg_scroller.speed
        if reward_rect.right < 0:
            reward_rect.left = WIDTH + 300

        # Check collisions
        enemy.check_collision_and_damage(player)
        if player.rect.colliderect(reward_rect):
            score += 1
            reward_rect.left = WIDTH + 300

        # Draw entities
        player.draw(screen)
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
