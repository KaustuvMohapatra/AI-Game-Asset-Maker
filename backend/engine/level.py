import pygame

class BackgroundScroller:
    def __init__(self, image, speed=2):
        self.image = image
        self.speed = speed
        self.x1 = 0
        self.x2 = image.get_width()

    def update(self):
        self.x1 -= self.speed
        self.x2 -= self.speed

        # Loop background
        if self.x1 <= -self.image.get_width():
            self.x1 = self.image.get_width()
        if self.x2 <= -self.image.get_width():
            self.x2 = self.image.get_width()

    def draw(self, screen):
        screen.blit(self.image, (self.x1, 0))
        screen.blit(self.image, (self.x2, 0))


def draw_score(screen, score, health=None):
    font = pygame.font.SysFont("Arial", 30)
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (20, 20))

    if health is not None:
        health_text = font.render(f"Health: {health}", True, (255, 100, 100))
        screen.blit(health_text, (20, 60))
