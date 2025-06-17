import pygame

class Enemy:
    def __init__(self, x, y, image):
        self.image = image
        self.rect = image.get_rect(topleft=(x, y))
        self.mask = pygame.mask.from_surface(image)

        self.speed = 4
        self.damage_cooldown = 1000  # milliseconds between damage
        self.last_damage_time = 0

    def move(self):
        self.rect.x -= self.speed

        # Reset position if off-screen (loop enemy)
        if self.rect.right < 0:
            self.rect.x = 960  # respawn off-screen right

        # Update mask if needed (animation support)
        self.mask = pygame.mask.from_surface(self.image)

    def check_collision_and_damage(self, player):
        offset = (player.rect.x - self.rect.x, player.rect.y - self.rect.y)
        overlap = self.mask.overlap(player.mask, offset)

        current_time = pygame.time.get_ticks()
        if overlap and current_time - self.last_damage_time > self.damage_cooldown:
            player.health -= 10
            self.last_damage_time = current_time
            print(f"[!! ENEMY HIT !!] Player damaged! Health: {player.health}")

    def draw(self, screen):
        screen.blit(self.image, self.rect)
