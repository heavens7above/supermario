import pygame
from ..config import *

class Player(pygame.sprite.Sprite):
    def __init__(self, jump_sound=None):
        super().__init__()
        self.image = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = SCREEN_HEIGHT - PLAYER_HEIGHT - 10
        self.velocity_y = 0
        self.jumping = False
        self.speed_x = 0
        self.facing_right = True
        self.animation_frame = 0
        self.animation_delay = 5
        self.animation_counter = 0
        self.jump_sound = jump_sound

    def update(self):
        # Apply gravity
        self.velocity_y += GRAVITY
        self.rect.y += self.velocity_y

        # Apply horizontal movement
        self.rect.x += self.speed_x

        # Update facing direction
        if self.speed_x > 0:
            self.facing_right = True
        elif self.speed_x < 0:
            self.facing_right = False

        # Animate player
        self.animation_counter += 1
        if self.animation_counter >= self.animation_delay:
            self.animation_counter = 0
            self.animation_frame = (self.animation_frame + 1) % 2
            self.image.fill(BLUE if self.animation_frame == 0 else RED)

        # Keep player on screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH

        # Ground collision (basic floor)
        if self.rect.bottom > SCREEN_HEIGHT - 10:
            self.rect.bottom = SCREEN_HEIGHT - 10
            self.velocity_y = 0
            self.jumping = False

    def jump(self):
        if not self.jumping:
            self.velocity_y = JUMP_POWER
            self.jumping = True
            if self.jump_sound:
                self.jump_sound.play()
