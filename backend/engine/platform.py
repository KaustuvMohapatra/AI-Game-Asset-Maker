import pygame

class Platform:
    def __init__(self, x, y, width, height, color=(100, 100, 100)):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = (100, 100, 255)

    def move(self, speed):
        self.rect.x -= speed
        if self.rect.right < 0:
            self.rect.left = 960 + 100  # Wrap around or reset offscreen

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
