import pygame

class Player:
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.mask = pygame.mask.from_surface(self.image)

        # Physics
        self.vel_y = 0
        self.jump = False
        self.gravity = 0.2
        self.jump_strength = -12
        self.ground_y = y  # Y-position of the ground

        # Stats
        self.health = 100

        # Lock x-position (side-scroller static player)
        self.start_x = x

    def handle_keys(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and not self.jump:
            self.vel_y = self.jump_strength
            self.jump = True

    def update(self, platforms=[]):
        self.vel_y += self.gravity
        self.rect.y += self.vel_y

    # Collision with platforms
        on_platform = False
        for plat in platforms:
            if self.rect.colliderect(plat.rect) and self.vel_y >= 0:
                if self.rect.bottom <= plat.rect.bottom + 10:
                    self.rect.bottom = plat.rect.top
                    self.vel_y = 0
                    self.jump = False
                    on_platform = True
                    break

    # If not on any platform, apply gravity
        if not on_platform and self.rect.bottom < self.ground_y:
            self.jump = True

    # Fall to ground if below platform level
        if self.rect.bottom >= self.ground_y:
            self.rect.bottom = self.ground_y
            self.vel_y = 0
            self.jump = False

    # Lock player x-position
        self.rect.x = 100
        self.mask = pygame.mask.from_surface(self.image)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def is_alive(self):
        return self.health > 0
