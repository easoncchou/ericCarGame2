import pygame


class Sprite(pygame.sprite.Sprite):
    def __init__(self, w: int, h: int, pos: tuple[int, int],
                 color: tuple[int, int, int]):
        # Call superclass constructor
        super().__init__()

        self.image = pygame.Surface([w, h])
        self.image.fill(color)

        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
