import pygame
import random
from pygame.math import Vector2

width = 600
height = 600
fps = 30
gameName = "Shooter"

pygame.init()
pygame.mixer.init()

BLACK = (0, 0, 0)
RED = (255, 0, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
Pink = (255, 20, 147)

imgdir = './media/img'
snddir = './media/snd'

screen = pygame.display.set_mode((width, height))

bg = pygame.image.load(imgdir + '/bg3.jpg')
bg = pygame.transform.scale(bg, (width, height))
bg_rect = bg.get_rect()

pygame.mixer.music.load(snddir + '/Music.wav')
pygame.mixer.music.play(loops = -1)
pygame.mixer.music.set_volume(0.1)


pygame.display.set_caption(gameName)
icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)

clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()

def drawText(screen, test, size, x, y, color):
    fontname = './calibri.ttf'
    font = pygame.font.Font(fontname, size)
    textsprite = font.render(test, True, color)
    textrect = textsprite.get_rect()
    textrect.center = (x, y)
    screen.blit(textsprite, textrect)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(imgdir + '/player/1.png')
        self.image = pygame.transform.scale(self.image, (100, 75))
        self.rect = self.image.get_rect()
        self.rect.center = (width/2, height/2)

        self.points = 0
        self.magazin = 10

        self.speed = 5
        self.copy = self.image
        self.position = Vector2(self.rect.center)
        self.angle = 0
        self.direction = Vector2(1, 0)

        self.anim_speed = 2
        self.frame = 0
        self.anim = []

        self.shoot_sound = pygame.mixer.Sound(snddir + '/shoot.wav')

        for i in range(1, 21):
            image = pygame.image.load(imgdir + f'./player/{i}.png')
            image = pygame.transform.scale(image, (100, 75))
            self.anim.append(image)


    def animation(self):
        self.image = self.anim[self.frame // self.anim_speed]
        self.frame += 1
        self.image = pygame.transform.rotate(self.image, self.angle)
        self.rect = self.image.get_rect(center = self.rect.center)

        if self.frame == self.anim_speed * len(self.anim):
            self.frame = 0


    def rotate(self, rotate_speed):
        self.direction.rotate_ip(-rotate_speed)
        self.angle += rotate_speed
        self.image = pygame.transform.rotate(self.copy, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)


    def update(self):
        self.animation()
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_RIGHT]:
            self.rotate(-5)
        if keystate[pygame.K_LEFT]:
            self.rotate(5)
        if keystate[pygame.K_UP]:
            self.position += self.speed * self.direction
        if keystate[pygame.K_DOWN]:
            self.position -= self.speed * self.direction

        self.rect.center = self.position

        if self.rect.right > width:     # Контроль правой границы
            self.rect.right = width

        if self.rect.left < 0:          # Контроль левой границы
            self.rect.left = 0

        if self.rect.top < 0:           # Контроль верхней границы
            self.rect.top = 0

        if self.rect.bottom > height:   # Контроль нижнейграницы
            self.rect.bottom = height

class Mob_left(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(imgdir + '/enemy5/grenade.png')
        self.image = pygame.transform.scale(self.image, (25, 30))
        self.rect = self.image.get_rect()

        self.rect.x = 0
        self.rect.y = random.randrange(0, width)

        self.speedx = random.randrange(1, 5)
        self.speedy = random.randrange(-5, 5)

        self.speed = 5
        self.copy = self.image
        self.position = Vector2(self.rect.center)
        self.angle = 0
        self.direction = Vector2(0, -1)
        self.hp = 0

        self.death_sound = pygame.mixer.Sound(snddir + '/zombie_death1.wav')

    def rotate(self, rotate_speed):
        self.direction.rotate_ip(-rotate_speed)
        self.angle += rotate_speed
        self.image = pygame.transform.rotate(self.copy, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def update(self):
        self.rotate(20)
        self.rect.x += random.randrange(1, 7)
        self.rect.y += random.randrange(1, 5)

        if self.rect.top < 0 or self.rect.right > width or self.rect.top > height:
            self.rect.x = 0
            self.rect.y = random.randrange(0, width)

            self.speedx = random.randrange(1, 5)
            self.speedy = random.randrange(-5, 5) #Uhfyfn

class Mob_right(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(imgdir + '/enemy1/1.png')
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()

        self.rect.x = height
        self.rect.y = random.randrange(0, height)

        self.speedx = random.randrange(1, 5)
        self.speedy = random.randrange(-1, 5)
        self.angle = 0

        self.anim_speed = 2
        self.frame = 0
        self.anim = []

        self.copy = self.image
        self.start = Vector2(0, 1)
        self.diretion = Vector2(self.speedx, self.speedy)
        self.angle = self.start.angle_to(self.diretion)
        self.image = pygame.transform.rotate(self.copy, -self.angle)

        self.hp = 100

        self.death_sound = pygame.mixer.Sound(snddir + '/zombie_death1.wav')

        for i in range(1, 10):
            image = pygame.image.load(imgdir + f'./enemy1/{i}.png')
            image = pygame.transform.scale(image, (50, 50))
            self.anim.append(image)

    def animation(self):
        self.image = self.anim[self.frame // self.anim_speed]
        self.frame += 1
        self.image = pygame.transform.rotate(self.image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

        if self.frame == self.anim_speed * len(self.anim):
            self.frame = 0


    def update(self):
        self.animation()
        self.rect.x -= random.randrange(1, 5)
        self.rect.y += random.randrange(-5, 5)

        if self.rect.top < 0 or self.rect.bottom > height or self.rect.top > height:
            self.rect.x = height
            self.rect.y = random.randrange(0, height)

            self.speedx = random.randrange(1, 5)
            self.speedy = random.randrange(-5, 5)

            self.diretion = Vector2(self.speedx, self.speedy)
            self.angle = self.start.angle_to(self.diretion)

class Mob_bottom(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(imgdir + '/enemy2/1.png')
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()

        self.rect.x = random.randrange(0, width)
        self.rect.y = height

        self.speedx = random.randrange(1, 5)
        self.speedy = random.randrange(-1, 5)
        self.angle = 0

        self.anim_speed = 2
        self.frame = 0
        self.anim = []
        self.hp = 0

        self.death_sound = pygame.mixer.Sound(snddir + '/zombie_death1.wav')

        for i in range(1, 10):
            image = pygame.image.load(imgdir + f'./enemy2/{i}.png')
            image = pygame.transform.scale(image, (50, 50))
            self.anim.append(image)

    def animation(self):
        self.image = self.anim[self.frame // self.anim_speed]
        self.frame += 1
        self.image = pygame.transform.rotate(self.image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

        if self.frame == self.anim_speed * len(self.anim):
            self.frame = 0

    def update(self):
        self.animation()
        self.rect.x += random.randrange(1, 7)
        self.rect.y += random.randrange(-5, 5)

        if self.rect.top < 0 or self.rect.left < 0 or self.rect.right > width:
            self.rect.x = random.randrange(0, width)
            self.rect.y = height

            self.speedx = random.randrange(1, 5)
            self.speedy = random.randrange(-1, 5)

class Bullet(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(imgdir + '/shell.png')
        self.image = pygame.transform.scale(self.image, (5, 15))

        self.image = pygame.transform.rotate(self.image, player.angle -90)
        self.rect = self.image.get_rect()

        self.rect.center = Vector2(player.rect.center)

        self.speed = 30
        self.move = player.direction * self.speed

    def update(self):
        self.rect.center += self.move

        if self.rect.x < 0 or self.rect.x > width or self.rect.y < 0 or self.rect.y > height:
            self.kill()

player = Player()
all_sprites.add(player)

for i in range(3):
    mob = Mob_left()
    all_sprites.add(mob)
    mobs.add(mob)

for i in range(3):
    mob_r = Mob_right()
    all_sprites.add(mob_r)
    mobs.add(mob_r)

for i in range(3):
    mob_bottom = Mob_bottom()
    all_sprites.add(mob_bottom)
    mobs.add(mob_bottom)

run = True
while run:
    clock.tick(fps)
    all_sprites.update()
    hits = pygame.sprite.spritecollide(player, mobs, False)
    shoots = pygame.sprite.groupcollide(bullets, mobs, True, False)
    if shoots:
        for mob in shoots.values():
            mob[0].hp -= 50
            if mob[0].hp < 0:
                mob[0].death_sound.play()
                mob[0].death_sound.set_volume(0.5)
                mob[0].kill()
                player.points += 10

    screen.blit(bg, bg_rect)
    all_sprites.draw(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if player.magazin > 0:
                    player.shoot_sound.play()
                    player.shoot_sound.set_volume(0.5)
                    bullet = Bullet()
                    all_sprites.add(bullet)
                    bullets.add(bullet)
                    player.magazin -= 1
            if event.key == pygame.K_r:
                player.magazin = 10



    drawText(screen, str(player.points), 30, 15, 20, RED)
    drawText(screen, str(player.magazin), 30, 50, 20, RED)
    pygame.display.flip()
pygame.quit()

