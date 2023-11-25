import pygame as pg
pg.init()
SCREEN_WIDTH, SCREEN_HEIGHT = 480, 640
BIRD_WIDTH = 50
BIRD_HEIGHT = 50
PIPE_WIDTH = 80
PIPE_GAP = 250
SPEED = 5
WHITE = (255, 255, 255)
GREEN = (0, 128, 0)
YELLOW = (255, 255, 0)
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

class Bird(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pg.Surface([BIRD_WIDTH, BIRD_HEIGHT])
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2))
        self.gravity = 1
        self.lift = -10
        self.velocity = 10

    def update(self):
        self.velocity += self.gravity
        self.rect.y += self.velocity

        if self.rect.top < 0:
            self.rect.top = 0
            self.velocity = 0

        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            self.velocity = 0

    def jump(self):
        self.velocity = self.lift

bird = Bird()

def main():
    clock = pg.time.Clock()
    while True:
        events = pg.event.get()
        for e in events:
            if e.type == pg.QUIT:
                return
            if e.type == pg.KEYDOWN:
                if e.type == pg.K_UP:
                    bird.jump()

        bird.update()
        screen.fill('white')
        screen.blit(bird.image, bird.rect)
        clock.tick(30)
        pg.display.update()
if __name__ == '__main__':
    main()