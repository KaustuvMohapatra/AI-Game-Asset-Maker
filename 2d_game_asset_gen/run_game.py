import pygame
import json
import os
from engine.player import Player
from engine.enemy import Enemy
from engine.level import draw_background, draw_score

pygame.init()
WIDTH, HEIGHT = 960, 540
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Generative Game")
clock = pygame.time.Clock()

# Load user config
with open("C:/nus_adv/config/game_config.json") as f:
    config = json.load(f)

# Load assets
def load_latest_image(folder):
    files = sorted(os.listdir(folder), reverse=True)
    if not files:
        raise Exception(f"No images found in {folder}")
    return pygame.image.load(os.path.join(folder, files[0]))

CHAR_IMG = pygame.transform.scale(load_latest_image("assets/characters"), (64, 64))
BG_IMG   = pygame.transform.scale(load_latest_image("assets/backgrounds"), (960, 540))
ENEMY_IMG = pygame.transform.scale(load_latest_image("assets/enemies"), (64, 64))
REWARD_IMG = pygame.transform.scale(load_latest_image("assets/rewards"), (32, 32))

# Entities
player = Player(100, HEIGHT - 100, CHAR_IMG)
enemy = Enemy(WIDTH, HEIGHT - 100, ENEMY_IMG)
reward_pos = pygame.Rect(WIDTH//2, HEIGHT - 90, 32, 32)
score = 0

def main():
    global score
    run = True
    while run:
        clock.tick(60)
        screen.fill((0, 0, 0))
        draw_background(screen, BG_IMG)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        player.handle_keys()
        player.update()
        enemy.move()

        screen.blit(REWARD_IMG, reward_pos)
        if player.rect.colliderect(reward_pos):
            score += 1
            reward_pos.x += 200  # Move reward

        player.draw(screen)
        enemy.draw(screen)
        draw_score(screen, score)

        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()