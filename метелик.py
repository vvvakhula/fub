import pygame
import random

pygame.init()

WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

class Butterfly(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('iconbf.png')
        self.image = pygame.transform.scale(self.image, (32, 32))
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (100, SCREEN_HEIGHT // 2)
        self.speed_y = 0
        self.hearts = 3  

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.speed_y = -5
        elif keys[pygame.K_DOWN]:
            self.speed_y = 5
        else:
            self.speed_y = 0

        self.rect.y += self.speed_y

        
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
        elif self.rect.top < 0:
            self.rect.top = 0

class Raindrop(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('iconrd.png')
        self.image = pygame.transform.scale(self.image, (32, 32))
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH
        self.rect.y = random.randrange(SCREEN_HEIGHT)

    def update(self):
        self.rect.x -= 5
        if self.rect.right < 0:
            self.rect.x = SCREEN_WIDTH
            self.rect.y = random.randrange(SCREEN_HEIGHT)

class Heart(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.image.load('heart.png')
        self.image = pygame.transform.scale(self.image, (32, 32))
        self.rect = self.image.get_rect()
        self.rect.topleft = pos

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Метелик")

background = pygame.image.load('background.jpg')
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

all_sprites = pygame.sprite.Group()
raindrops = pygame.sprite.Group()
hearts = pygame.sprite.Group()

butterfly = Butterfly()
all_sprites.add(butterfly)

for i in range(3):
    heart = Heart((10 + i * 40, 10))
    hearts.add(heart)

for i in range(10):
    raindrop = Raindrop()
    all_sprites.add(raindrop)
    raindrops.add(raindrop)

running = True
game_over = False  
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if not game_over:
        all_sprites.update()

        hits = pygame.sprite.spritecollide(butterfly, raindrops, True)

        if hits:
            butterfly.hearts -= 1
            if butterfly.hearts < 0:
                game_over = True
            else:
                hearts.remove(hearts.sprites()[-1])

        screen.blit(background, (0, 0))

        all_sprites.draw(screen)
        hearts.draw(screen)
        pygame.display.flip()

        pygame.time.delay(30)
    else:
        screen.fill(WHITE)
        font = pygame.font.Font(None, 36)
        text = font.render("Гра завершена!", True, (255, 0, 0))
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(text, text_rect)
        pygame.display.flip()
        pygame.time.delay(2000)  

pygame.quit()
