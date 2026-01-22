import pygame
import os
import random
import asyncio
from .config import *
from .sprites import Player, Platform, Coin

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Simple Mario Game")
        self.clock = pygame.time.Clock()
        self.running = True
        self.score = 0
        self.font = pygame.font.Font(None, 36)
        
        self.load_assets()
        self.create_sprites()

    def load_assets(self):
        # Resolve assets directory relative to this file
        current_dir = os.path.dirname(os.path.abspath(__file__))
        base_path = os.path.join(current_dir, "assets")
        
        try:
            self.jump_sound = pygame.mixer.Sound(os.path.join(base_path, 'sounds', 'jump.wav'))
            self.coin_sound = pygame.mixer.Sound(os.path.join(base_path, 'sounds', 'coin.wav'))
        except Exception as e:
            print(f"Warning: Sound files not found ({e}). Game will run without sound effects.")
            self.jump_sound = None
            self.coin_sound = None

    def create_sprites(self):
        self.all_sprites = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        self.coins = pygame.sprite.Group()
        
        self.player = Player(self.jump_sound)
        self.all_sprites.add(self.player)

        # Create platforms
        platform_list = [
            Platform(0, SCREEN_HEIGHT - 10, SCREEN_WIDTH, 10),  # Ground
            Platform(300, 400, 200, 20),
            Platform(100, 300, 200, 20),
            Platform(500, 200, 200, 20),
        ]

        for platform in platform_list:
            self.all_sprites.add(platform)
            self.platforms.add(platform)

        # Create coins
        for _ in range(5):
            self.spawn_coin()

    def spawn_coin(self):
        coin = Coin(random.randint(0, SCREEN_WIDTH - 20),
                    random.randint(100, SCREEN_HEIGHT - 100))
        self.all_sprites.add(coin)
        self.coins.add(coin)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.player.jump()
                elif event.key == pygame.K_ESCAPE:
                    self.running = False

        keys = pygame.key.get_pressed()
        self.player.speed_x = (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * PLAYER_SPEED

    def update(self):
        self.all_sprites.update()

        # Platform collisions
        hits = pygame.sprite.spritecollide(self.player, self.platforms, False)
        if hits:
            # Simple collision logic: if falling and hit top
            if self.player.velocity_y > 0:
                 if self.player.rect.bottom <= hits[0].rect.bottom: # ensure we are above
                    self.player.rect.bottom = hits[0].rect.top
                    self.player.velocity_y = 0
                    self.player.jumping = False

        # Coin collisions
        coin_hits = pygame.sprite.spritecollide(self.player, self.coins, True)
        for coin in coin_hits:
            self.score += 10
            if self.coin_sound:
                self.coin_sound.play()
            self.spawn_coin()

    def draw(self):
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        
        score_text = self.font.render(f'Score: {self.score}', True, WHITE)
        self.screen.blit(score_text, (10, 10))
        
        pygame.display.flip()

    async def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
            await asyncio.sleep(0)
        pygame.quit()
