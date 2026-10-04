import asyncio
import random

import pygame

WIDTH = 960
HEIGHT = 640
TITLE = "Moonbounce"

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()
font = pygame.font.Font(None, 100)

background = pygame.image.load("images/background.png").convert()
moon_image = pygame.image.load("images/moon.png").convert_alpha()
moon = moon_image.get_rect(center=(WIDTH / 2, HEIGHT / 2))

min_speed = 1
max_speed = 5
speed_x = random.randint(1, 5) * (random.randint(0, 1) * 2 - 1)
speed_y = random.randint(-5, 5)
score = 0
next_speed_increase = 10


def handle_click(pos):
    global score, min_speed, max_speed, next_speed_increase

    if moon.collidepoint(pos):
        score += 1
        if score == next_speed_increase:
            min_speed += 1
            max_speed += 1
            next_speed_increase += 10
    else:
        score -= 1


def bounce():
    global speed_x, speed_y

    if moon.right >= WIDTH:
        speed_x = random.randint(-max_speed, -min_speed)
        speed_y = random.randint(-max_speed, max_speed)

    if moon.top <= 0:
        speed_x = random.randint(-max_speed, max_speed)
        speed_y = random.randint(min_speed, max_speed)

    if moon.left <= 0:
        speed_x = random.randint(min_speed, max_speed)
        speed_y = random.randint(-max_speed, max_speed)

    if moon.bottom >= HEIGHT:
        speed_x = random.randint(-max_speed, max_speed)
        speed_y = random.randint(-max_speed, -min_speed)

    moon.x += speed_x
    moon.y += speed_y


def draw():
    screen.blit(background, (0, 0))
    screen.blit(moon_image, moon)
    score_surface = font.render(f"Score: {score}", True, "lightblue")
    screen.blit(score_surface, (90, 60))
    pygame.display.flip()


async def main():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                handle_click(event.pos)

        bounce()
        draw()
        clock.tick(60)
        await asyncio.sleep(0)

    pygame.quit()


asyncio.run(main())
