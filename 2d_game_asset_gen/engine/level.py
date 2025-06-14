import pygame
def draw_background(screen, bg_img):
    screen.blit(bg_img, (0, 0))

def draw_score(screen, score):
    font = pygame.font.SysFont("Arial", 30)
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (20, 20))