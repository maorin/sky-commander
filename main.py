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
        self.lives = 3  # 玩家初始有3条生命
        self.invincible = False  # 是否无敌（被撞后短暂无敌）
        self.invincible_timer = 0  # 无敌时间计时器

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
            
        # 处理无敌状态
        if self.invincible:
            self.invincible_timer -= 1
            if self.invincible_timer <= 0:
                self.invincible = False

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

        # 检查玩家与敌机的碰撞
        if not player.invincible:  # 只有在非无敌状态下才检测碰撞
            hits = pygame.sprite.spritecollide(player, enemies, False)
            if hits:
                player.lives -= 1  # 减少一条生命
                
                # 如果生命值为0，游戏结束
                if player.lives <= 0:
                    running = False  # Game over
                else:
                    # 否则，让玩家短暂无敌
                    player.invincible = True
                    player.invincible_timer = 120  # 2秒无敌(60帧/秒 * 2秒)
                    
                    # 移除碰撞的敌机
                    for enemy in hits:
                        enemy.kill()
                        new_enemy = Enemy()
                        all_sprites.add(new_enemy)
                        enemies.add(new_enemy)

        # Draw / render
        screen.fill(black)
        screen.blit(background_img, (0, 0))
        draw_score(screen, score)
        draw_lives(screen, player.lives)  # 绘制生命值
        
        # 无敌状态下闪烁显示玩家
        if player.invincible and pygame.time.get_ticks() % 200 < 100:
            # 如果在无敌状态且时间为偶数帧，不绘制玩家
            temp_sprites = pygame.sprite.Group([sprite for sprite in all_sprites if sprite != player])
            temp_sprites.draw(screen)
        else:
            all_sprites.draw(screen)
            
        pygame.display.flip()

def draw_score(surf, score):
    font = pygame.font.Font(None, 36)
    text = font.render("Score: " + str(score), True, white)
    text_rect = text.get_rect()
    surf.blit(text, text_rect)

def draw_lives(surf, lives):
    # 绘制生命值（红心）
    heart_width = 30
    heart_height = 30
    heart_spacing = 10
    for i in range(lives):
        # 创建一个红色的心形图像
        heart = pygame.Surface((heart_width, heart_height))
        heart.fill((0, 0, 0))  # 透明背景
        heart.set_colorkey((0, 0, 0))
        pygame.draw.polygon(heart, red, [(heart_width//2, heart_height//5), 
                                        (heart_width//5, heart_height//2), 
                                        (heart_width//2, heart_height-heart_height//5), 
                                        (heart_width-heart_width//5, heart_height//2)])
        pygame.draw.circle(heart, red, (heart_width//3, heart_height//3), heart_width//4)
        pygame.draw.circle(heart, red, (heart_width-heart_width//3, heart_height//3), heart_width//4)
        
        # 在屏幕右上角显示
        x = screen_width - (i + 1) * (heart_width + heart_spacing)
        y = 10
        surf.blit(heart, (x, y))


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
    # 重置游戏状态
    score = 0  # 重置分数
    
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
