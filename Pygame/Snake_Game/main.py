# Snake  # Version 0.2

import pygame
import time
import random

pygame.init()  # инициализация инструментов pygame


def snake(headname, bodyname, snakeList, lead_x, lead_y):  #
    for XnY in snakeList:
        gameDisplay.blit(pygame.image.load(bodyname), (XnY[0], XnY[1]))  #
    gameDisplay.blit(pygame.image.load(headname), (lead_x, lead_y))  #


def message_to_screen(msg, color, x, y):
    screen_text = font.render(msg, True, color)
    gameDisplay.blit(screen_text, [x, y])


def new_item():
    coordinates = []
    X = int(random.randrange(display_width - block_size) / block_size) * block_size
    Y = int(random.randrange(display_height - block_size) / block_size) * block_size
    coordinates.append(X)
    coordinates.append(Y)
    return coordinates


def collision_checking(obj1_X, obj1_Y, obj2_X, obj2_Y):
    if obj1_X == obj2_X and obj1_Y == obj2_Y:
        return True
    else:
        return False


def draw_objects():
    gameDisplay.blit(pygame.image.load('bg.png'), (0, 0))  #
    # отображение яблока
    gameDisplay.blit(pygame.image.load('apple.png'), (apple_coordinates[0], apple_coordinates[1]))  #
    # отображение монетки
    gameDisplay.blit(pygame.image.load('mushroom.png'), (mushroom_coordinates[0], mushroom_coordinates[1]))  #
    # отображение змейки
    snake('head.png', 'body.png', snakeList, lead_x, lead_y)  #
    # отображение количества очков
    message_to_screen(''.join(["Score: ", str(score)]), white, 10, 10)

    pygame.display.update()
    pygame.time.delay(time_speed_delay)


# Константы
white = (255, 255, 255)

display_width = 600  #
display_height = 600  #
block_size = 40  #
time_speed_delay = 150

# Объекты: шрифт, окно игры, капча
font = pygame.font.SysFont('Arial', 32)
gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("Snake")
icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)

run_game = True

# Спавн змеи:
# в рандомном месте
lead_x = int(random.randrange(display_width - block_size) / block_size) * block_size  #
lead_y = int(random.randrange(display_height - block_size) / block_size) * block_size  #
# или в середине экрана
# lead_x = (display_width // block_size) // 2 * block_size
# lead_y = (display_width // block_size) // 2 * block_size

lead_x_change = 0
lead_y_change = 0

snakeList = []
snakeLength = 1
score = 0

apple_coordinates = new_item()
mushroom_coordinates = new_item()

# Создание звуков
pygame.mixer.init()  # инициализация звукового модуля mixer
sound_apple = pygame.mixer.Sound('apple.wav')
sound_mushroom = pygame.mixer.Sound('mushroom.wav')
sound_hit = pygame.mixer.Sound('hit.wav')

# Музыка
pygame.mixer.music.load('Schnappi.ogg')

# Воспроизведение музыки
pygame.mixer.music.play()  # параметр, переданный функции — количество воспроизведений

while run_game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run_game = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and lead_x_change == 0:
                lead_x_change = -block_size
                lead_y_change = 0
            elif event.key == pygame.K_RIGHT and lead_x_change == 0:
                lead_x_change = block_size
                lead_y_change = 0
            elif event.key == pygame.K_DOWN and lead_y_change == 0:
                lead_x_change = 0
                lead_y_change = block_size
            elif event.key == pygame.K_UP and lead_y_change == 0:
                lead_x_change = 0
                lead_y_change = -block_size

    # движение змейки
    lead_x += lead_x_change
    lead_y += lead_y_change

    # прохождение насквозь(телепортация)
    if lead_x > display_width - block_size:  # правая стена телепортирует к левой
        lead_x = 0  # 0
    elif lead_x < 0:
        lead_x = display_width - block_size
    elif lead_y > display_height - block_size:
        lead_y = 0  # 0
    elif lead_y < 0:
        lead_y = display_height - block_size

    # Сборка змеи
    snakeHead = [lead_x, lead_y]
    snakeList.append(snakeHead)
    if len(snakeList) > snakeLength:
        del snakeList[0]

    # столкновение с яблоком
    if collision_checking(lead_x, lead_y, apple_coordinates[0], apple_coordinates[1]):
        apple_coordinates = new_item()
        snakeLength += 1
        score += 1
        sound_apple.play()  # воспроизведение звука поедания яблока

    # столкновение с грибом
    if collision_checking(lead_x, lead_y, mushroom_coordinates[0], mushroom_coordinates[1]):
        mushroom_coordinates = new_item()
        score += 3
        if time_speed_delay > 50:
            time_speed_delay -= 5
        sound_mushroom.play()  # воспроизведение звука поедания гриба

    # столкновение змейки с самой собой
    for eachSegment in snakeList[:-1]:
        if eachSegment == snakeHead:
            gameDisplay.blit(pygame.image.load('bg.png'), (0, 0))
            message_to_screen(''.join(["Game over! Score: ", str(score)]), white, 200, 260)
            pygame.display.update()
            time.sleep(2)
            run_game = False
            sound_hit.play()

    draw_objects()
    # gameDisplay.blit(pygame.image.load('bg.png'), (0, 0))  #
    # отображение змейки
    # snake('head.png', 'body.png', snakeList, lead_x, lead_y)  #

    # pygame.display.update()
    # pygame.time.delay(time_speed_delay)

pygame.quit()


