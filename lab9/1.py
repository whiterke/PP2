import pygame
import random

pygame.init()

HEIGHT = 600
WIDTH = 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

road = pygame.image.load("resources/AnimatedStreet.png")
coin_i = pygame.image.load("resources/Coin.png")
player_im = pygame.image.load("resources/Player.png")
enemy_im = pygame.image.load("resources/Enemy.png")

pygame.mixer.music.load('resources/background.wav')
pygame.mixer.music.play(-1)
coin_sound = pygame.mixer.Sound('resources/coin.mp3')

font = pygame.font.SysFont("Verdana", 30)
count = 0

COIN_THRESHOLD = 5
enemy_upgrade_level = 0

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_im
        self.speed = 5
        self.rect = self.image.get_rect()
        self.rect.midbottom = (WIDTH // 2, HEIGHT)
    
    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            self.rect.move_ip(self.speed, 0)
        if keys[pygame.K_LEFT]:
            self.rect.move_ip(-self.speed, 0)
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH

class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.base_image = coin_i  
        self.generate() 

    def generate(self):
        self.weight = random.randint(1, 3)
        if self.weight == 1:
            size = 50
        elif self.weight == 2:
            size = 75
        else:
            size = 100
        self.image = pygame.transform.scale(self.base_image, (size, size))
        self.rect = self.image.get_rect()
        self.speed = 5 + self.weight * 2
        self.rect.left = random.randint(0, WIDTH - self.rect.width)
        self.rect.bottom = 0

    def move(self):
        self.rect.move_ip(0, self.speed)
        if self.rect.top > HEIGHT:
            self.generate()

class Enemy(pygame.sprite.Sprite):
    def __init__(self, speed=5):
        super().__init__()
        self.image = enemy_im
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.left = random.randint(0, WIDTH - self.rect.width)
        self.rect.top = 0
    
    def move(self):
        self.rect.move_ip(0, self.speed)
        if self.rect.top > HEIGHT:
            self.reset_pos()

    def reset_pos(self):
        self.rect.left = random.randint(0, WIDTH - self.rect.width)
        self.rect.top = 0

player = Player()
coin = Coin()
enemy = Enemy(speed=5)

all_sprites = pygame.sprite.Group(player, coin, enemy)
coin_sprites = pygame.sprite.Group(coin)
enemy_sprites = pygame.sprite.Group(enemy)

running = True
game_over = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if not game_over:
        player.move()
        coin.move()
        enemy.move()
    
        if pygame.sprite.spritecollideany(player, coin_sprites):
            coin_sound.play()

            count += coin.weight
            coin.generate()  

            if count // COIN_THRESHOLD > enemy_upgrade_level:
                enemy_upgrade_level = count // COIN_THRESHOLD
                enemy.speed += 1

        if pygame.sprite.spritecollideany(player, enemy_sprites):
            game_over = True

    screen.blit(road, (0, 0))
    all_sprites.draw(screen)
    
    score_text = font.render(f"Score: {count}", True, (0, 0, 0))
    screen.blit(score_text, (10, 10))
    
    if game_over:
        over_text = font.render("Game Over!", True, (255, 0, 0))
        screen.blit(over_text, ((WIDTH - over_text.get_width()) // 2, (HEIGHT - over_text.get_height()) // 2))
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
