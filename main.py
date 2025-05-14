import pygame
import random
import os

# Initialize Pygame
pygame.init()

# Screen dimensions
screen_width = 960  # Example width
screen_height = 540 # Corresponding height for 16:9
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Space Shooter")

# Score
score = 0

# Colors
white = (255, 255, 255)  # White for bullets
black = (0, 0, 0)      # Black background
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

# Load images (replace with your own images)
try:
    assets_dir = os.path.join(os.path.dirname(__file__), "assets")
    
    try:
        player_img = pygame.image.load(os.path.join(assets_dir, "player.png")).convert_alpha()
    except FileNotFoundError:
        print("Error: Could not load player.png. Using placeholder.")
        player_img = pygame.Surface((50, 38))
        player_img.fill(blue)
    try:
        enemy_img = pygame.image.load(os.path.join(assets_dir, "enemy.png")).convert_alpha()
    except FileNotFoundError:
        print("Error: Could not load enemy.png. Using placeholder.")
        enemy_img = pygame.Surface((30, 20))
        enemy_img.fill(red)
    try:
        bullet_img = pygame.image.load(os.path.join(assets_dir, "bullet.png")).convert_alpha()
    except FileNotFoundError:
        print("Error: Could not load bullet.png. Using placeholder.")
        bullet_img = pygame.Surface((5, 10))
        bullet_img.fill(white)
    background_img = pygame.Surface((screen_width, screen_height))
    background_img.fill(black)
except FileNotFoundError:
    enemy_img = pygame.Surface((30, 20))
    
    enemy_img.fill(red)
    bullet_img = pygame.Surface((5, 10))
    bullet_img.fill(white)
    background_img = pygame.Surface((screen_width, screen_height))
    background_img.fill(black)


# Scale images if needed
player_img = pygame.transform.scale(player_img, (64, 64))
enemy_img = pygame.transform.scale(enemy_img, (60, 40))
bullet_img = pygame.transform.scale(bullet_img, (5, 10))
background_img = pygame.transform.scale(background_img, (screen_width, screen_height))

# Rotate images for horizontal orientation
# enemy_img = pygame.transform.rotate(enemy_img, 90)


# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = player_img
        self.rect = self.image.get_rect()
        self.rect.centery = screen_height // 2
        self.rect.left = 10
        self.speedy = 0

    def update(self):
        self.speedy = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_UP]:
            self.speedy = -5
        if keystate[pygame.K_DOWN]:
            self.speedy = 5
        self.rect.y += self.speedy
        if self.rect.bottom > screen_height:
            self.rect.bottom = screen_height
        if self.rect.top < 0:
            self.rect.top = 0

    def shoot(self):
        bullet = Bullet(self.rect.right, self.rect.centery)
        all_sprites.add(bullet)
        bullets.add(bullet)


# Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = enemy_img
        self.rect = self.image.get_rect()
        self.rect.y = random.randrange(screen_height - self.rect.height)
        self.rect.x = random.randrange(screen_width, screen_width + 100)
        self.speedx = random.randrange(-8, -1)
        self.speedy = random.randrange(-3, 3)

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.left < -25 or self.rect.top > screen_height + 10 or self.rect.bottom < -10:
            self.rect.y = random.randrange(screen_height - self.rect.height)
            self.rect.x = random.randrange(screen_width, screen_width + 100)
            self.speedx = random.randrange(-8, -1)


# Bullet class
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.left = x
        self.rect.centery = y
        self.speedx = 10

    def update(self):
        self.rect.x += self.speedx
        if self.rect.left > screen_width:
            self.kill()


# Sprite groups
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()

player = Player()
all_sprites.add(player)
for i in range(8):
    enemy = Enemy()
    all_sprites.add(enemy)
    enemies.add(enemy)

# Game loop
clock = pygame.time.Clock()


def show_start_menu():
    title_font = pygame.font.Font(None, 74)
    instruction_font = pygame.font.Font(None, 36)
    title_text = title_font.render("Space Shooter", True, white)
    instruction_text = instruction_font.render("Press Space to Start", True, white)
    title_rect = title_text.get_rect(center=(screen_width // 2, screen_height // 2 - 50))
    instruction_rect = instruction_text.get_rect(center=(screen_width // 2, screen_height // 2 + 50))

    running = True
    while running:
        screen.fill(black)
        screen.blit(title_text, title_rect)
        screen.blit(instruction_text, instruction_rect)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    running = False


def game_loop():
    global score
    running = True
    while running:
        clock.tick(60)  # 60 FPS

        # Process events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.shoot()

        # Update
        all_sprites.update()

        # Check for collisions
        hits = pygame.sprite.groupcollide(enemies, bullets, True, True)
        for hit in hits:
            score += 1
            enemy = Enemy()
            all_sprites.add(enemy)
            enemies.add(enemy)

        hits = pygame.sprite.spritecollide(player, enemies, False)
        if hits:
            running = False  # Game over on collision

        # Draw / render
        screen.fill(black)
        screen.blit(background_img, (0, 0))
        draw_score(screen, score)
        all_sprites.draw(screen)
        pygame.display.flip()

def draw_score(surf, score):
    font = pygame.font.Font(None, 36)
    text = font.render("Score: " + str(score), True, white)
    text_rect = text.get_rect()
    surf.blit(text, text_rect)


def show_game_over():
    game_over_font = pygame.font.Font(None, 74)
    instruction_font = pygame.font.Font(None, 36)
    game_over_text = game_over_font.render("Game Over", True, white)
    instruction_text = instruction_font.render("Press Space to Restart or Q to Quit", True, white)
    game_over_rect = game_over_text.get_rect(center=(screen_width // 2, screen_height // 2 - 50))
    instruction_rect = instruction_text.get_rect(center=(screen_width // 2, screen_height // 2 + 50))

    running = True
    while running:
        screen.fill(black)
        screen.blit(game_over_text, game_over_rect)
        screen.blit(instruction_text, instruction_rect)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                running = False


show_start_menu()
while True:
    all_sprites = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    bullets = pygame.sprite.Group()

    player = Player()
    all_sprites.add(player)
    for i in range(8):
        enemy = Enemy()
        all_sprites.add(enemy)
        enemies.add(enemy)
    game_loop()
    show_game_over()
