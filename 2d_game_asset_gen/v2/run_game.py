import pygame
import json
import os
from engine.player import Player
from engine.enemy import Enemy
from engine.level import draw_background, draw_score

# Initialize Pygame
pygame.init()
WIDTH, HEIGHT = 960, 540
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Generative Game")
clock = pygame.time.Clock()

# Load config
with open("C:/nus_adv/config/game_config.json") as f:
    config = json.load(f)

# Utility to load latest image from a folder
def load_latest_image(folder):
    files = sorted(os.listdir(folder), reverse=True)
    if not files:
        raise Exception(f"No images found in {folder}")
    img_path = os.path.join(folder, files[0])
    return load_image_make_transparent(img_path)

def load_image_make_transparent(path, colorkey=None):
    image = pygame.image.load(path).convert()
    if colorkey is None:
        # Default: assume white (255,255,255) is background to make transparent
        colorkey = (255, 255, 255)
    image.set_colorkey(colorkey)
    return image.convert_alpha()



# Load assets with transparency
CHAR_IMG = pygame.transform.smoothscale(load_latest_image("assets/characters"), (64, 64)).convert_alpha()
BG_IMG = pygame.transform.smoothscale(load_latest_image("assets/backgrounds"), (960, 540)).convert_alpha()
ENEMY_IMG = pygame.transform.smoothscale(load_latest_image("assets/enemies"), (64, 64)).convert_alpha()
REWARD_IMG = pygame.transform.smoothscale(load_latest_image("assets/rewards"), (32, 32)).convert_alpha()

# Initialize game entities
player = Player(100, HEIGHT - 100, CHAR_IMG)
enemy = Enemy(WIDTH, HEIGHT - 100, ENEMY_IMG)
reward_pos = pygame.Rect(WIDTH // 2, HEIGHT - 90, 32, 32)
score = 0

# Font for HUD
font = pygame.font.SysFont(None, 32)

def draw_hud():
    # Score
    draw_score(screen, score)
    # Health
    health_text = font.render(f"Health: {player.health}", True, (255, 100, 100))
    screen.blit(health_text, (20, 40))

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

        # Player input & update
        player.handle_keys()
        player.update()

        # Enemy movement & damage check
        enemy.move()
        enemy.check_collision_and_damage(player)

        # Reward logic
        screen.blit(REWARD_IMG, reward_pos)
        if player.rect.colliderect(reward_pos):
            score += 1
            reward_pos.x += 200
            if reward_pos.x > WIDTH:
                reward_pos.x = 100

        # Draw all entities
        player.draw(screen)
        enemy.draw(screen)
        draw_hud()

        # Game over condition
        if player.health <= 0:
            print("Game Over!")
            run = False

        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()
