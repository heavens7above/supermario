import pygame
from ..config import GOLD, ORANGE

class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill(GOLD)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.animation_frame = 0
        self.animation_delay = 10
        self.animation_counter = 0

    def update(self):
        self.animation_counter += 1
        if self.animation_counter >= self.animation_delay:
            self.animation_counter = 0
            self.animation_frame = (self.animation_frame + 1) % 2
            self.image.fill(GOLD if self.animation_frame == 0 else ORANGE)
