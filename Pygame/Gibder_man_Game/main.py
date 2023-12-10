import random
import pygame
pygame.init()

def draw_text(sccreen, text, size, x, y, color):
    font_name = pygame.font.match_font('arial')
    font = pygame.font.Font(font_name, size)
    text_image = font.render(text, True, color)
    text_rect = text_image.get_rect()
    text_rect.center = (x, y)
    sccreen.blit(text_image, text_rect)

widtch = 1200
height = 800
fps = 30
game_name = "Arcanoid"

GREEN = "#008000"       # Зеленый RGB
BLUE = "#0000FF"        # Синий
CYAN = "#00FFFF"        # Голубой

screen = pygame.display.set_mode((widtch, height))
pygame.display.set_caption(game_name)

icon = pygame.image.load('./icons/santa-claus.png')
pygame.display.set_icon(icon)

# Задник :)
bg = pygame.image.load('./icons/bg.jpg')
bg_rect = bg.get_rect()


# 1 спрайт
size_gingerbread_man = (100, 100)
pic = pygame.image.load('./icons/gingerbread-man.png')
pic = pygame.transform.scale(pic, size_gingerbread_man)
pic_rect = pic.get_rect()

# 2 спрайт
racket = pygame.image.load('./icons/rocket.png')
racket_rect = racket.get_rect()
racket_rect.x = widtch / 2 - racket.get_width() / 2
racket_rect.y = height - 50


speedx = 10
speedy = 10

lives = 3   # Количество жизней

pygame.mixer.music.load('./snd/Ludum Dare 38 - Track 2.wav')
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(-1)

ping = pygame.mixer.Sound('./snd/Jump 1.wav')
loose = pygame.mixer.Sound('./snd/Retro Negative Short 23.wav')


timer = pygame.time.Clock()
run = True

while run:  # Начинаем бесконечный цикл
    timer.tick(fps)  # Контроль времени (обновление игры)
    for event in pygame.event.get():  # Обработка ввода (события)
        if event.type == pygame.QUIT:  # Проверить закрытие окна
            run = False  # Завершаем игровой цикл

    key = pygame.key.get_pressed()
    if key[pygame.K_LEFT] and racket_rect.left > 0:
        racket_rect.x -= 10
    if key[pygame.K_RIGHT] and racket_rect.right < widtch:
        racket_rect.x += 10

    # Рендеринг (прорисовка)
    # screen.fill(CYAN)  # Заливка заднего фона
    screen.blit(bg, bg_rect)
    screen.blit(pic, pic_rect)

    draw_text(screen, 'Livenes: ' + str(lives), 30, widtch // 2, 30, GREEN)

    pic_rect.x += speedx  # Увеличиваем координату Х спрайта
    pic_rect.y += speedy  # Увеличиваем координату Y спрайта

    #bg_rect.x -= 2
    #if bg_rect.x <= -widtch:
    #    bg_rect.x = 0

    if pic_rect.bottom > height:  # Если достигли нижней границы экрана
        lives -= 1
        pic_rect.y = 0
        pic_rect.x = random.randint(0, widtch)
        loose.play()
        if lives == 0:
            run = False
            print('Игра закончена!')

    if pic_rect.top < 0:  # Если достигли верхней границы экрана
        speedy = -speedy
        ping.play()
    if pic_rect.left < 0:  # Если достигли левой границы экрана
        speedx = -speedx
        ping.play()
    if pic_rect.right > widtch:  # Если достигли правой границы экрана
        speedx = -speedx
        ping.play()

    if pic_rect.colliderect(racket_rect):
        speedy = -speedy
        ping.play()

    screen.blit(racket, racket_rect)
    pygame.display.update()  # Переворачиваем экран









