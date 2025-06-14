import pygame

class Player:
    def __init__(self, x, y, image):
        self.image = image
        self.rect = pygame.Rect(x, y, image.get_width(), image.get_height())
        self.vel_y = 0
        self.jump = False

    def handle_keys(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= 5
        if keys[pygame.K_RIGHT]:
            self.rect.x += 5
        if keys[pygame.K_SPACE] and not self.jump:
            self.vel_y = -12
            self.jump = True

    def update(self):
        self.vel_y += 0.5  # Gravity
        self.rect.y += self.vel_y

        if self.rect.y >= 400:
            self.rect.y = 400
            self.vel_y = 0
            self.jump = False

    def draw(self, screen):
        screen.blit(self.image, self.rect)