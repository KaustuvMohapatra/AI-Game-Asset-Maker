class Enemy:
    def __init__(self, x, y, image):
        self.image = image
        self.rect = image.get_rect(topleft=(x, y))

    def move(self):
        self.rect.x -= 3
        if self.rect.right < 0:
            self.rect.x = 960

    def draw(self, screen):
        screen.blit(self.image, self.rect)