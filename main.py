import pygame
import os
import sys
import random
import asyncio

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Player properties
PLAYER_WIDTH = 40
PLAYER_HEIGHT = 60
PLAYER_SPEED = 5
JUMP_POWER = -15
GRAVITY = 0.8

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Simple Mario Game")
clock = pygame.time.Clock()

# Load sound effects
try:
    JUMP_SOUND = pygame.mixer.Sound(os.path.join('assets', 'sounds', 'jump.wav'))
    COIN_SOUND = pygame.mixer.Sound(os.path.join('assets', 'sounds', 'coin.wav'))
except:
    print("Warning: Sound files not found. Game will run without sound effects.")
    JUMP_SOUND = None
    COIN_SOUND = None

class Player(pygame.sprite.Sprite):
    def __init__(self):
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

        # Ground collision
        if self.rect.bottom > SCREEN_HEIGHT - 10:
            self.rect.bottom = SCREEN_HEIGHT - 10
            self.velocity_y = 0
            self.jumping = False

    def jump(self):
        if not self.jumping:
            self.velocity_y = JUMP_POWER
            self.jumping = True
            if JUMP_SOUND:
                JUMP_SOUND.play()

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill((255, 215, 0))  # Gold color
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
            self.image.fill((255, 215, 0) if self.animation_frame == 0 else (255, 165, 0))

async def main():
    # Create sprite groups
    all_sprites = pygame.sprite.Group()
    platforms = pygame.sprite.Group()
    coins = pygame.sprite.Group()
    player = Player()

    # Add sprites to groups
    all_sprites.add(player)

    # Create some platforms
    platform_list = [
        Platform(0, SCREEN_HEIGHT - 10, SCREEN_WIDTH, 10),  # Ground
        Platform(300, 400, 200, 20),  # Platform 1
        Platform(100, 300, 200, 20),  # Platform 2
        Platform(500, 200, 200, 20),  # Platform 3
    ]

    for platform in platform_list:
        all_sprites.add(platform)
        platforms.add(platform)

    # Create coins
    for _ in range(5):
        coin = Coin(random.randint(0, SCREEN_WIDTH - 20),
                    random.randint(100, SCREEN_HEIGHT - 100))
        all_sprites.add(coin)
        coins.add(coin)

    # Score
    score = 0
    font = pygame.font.Font(None, 36)

    # Game loop
    running = True
    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.jump()
                elif event.key == pygame.K_ESCAPE:
                    running = False

        # Get keyboard state
        keys = pygame.key.get_pressed()
        player.speed_x = (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * PLAYER_SPEED

        # Update
        all_sprites.update()

        # Platform collisions
        hits = pygame.sprite.spritecollide(player, platforms, False)
        if hits:
            player.rect.bottom = hits[0].rect.top
            player.velocity_y = 0
            player.jumping = False

        # Coin collisions
        coin_hits = pygame.sprite.spritecollide(player, coins, True)
        for coin in coin_hits:
            score += 10
            if COIN_SOUND:
                COIN_SOUND.play()
            # Create new coin
            new_coin = Coin(random.randint(0, SCREEN_WIDTH - 20),
                           random.randint(100, SCREEN_HEIGHT - 100))
            all_sprites.add(new_coin)
            coins.add(new_coin)

        # Draw
        screen.fill(BLACK)
        all_sprites.draw(screen)
        
        # Draw score
        score_text = font.render(f'Score: {score}', True, WHITE)
        screen.blit(score_text, (10, 10))
        
        pygame.display.flip()

        # Cap the framerate
        clock.tick(FPS)
        await asyncio.sleep(0)

    pygame.quit()
    sys.exit()

asyncio.run(main()) 
