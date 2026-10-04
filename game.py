import pgzrun
import random

WIDTH = 960
HEIGHT = 640
TITLE = "Moonbounce"

moon = Actor("moon", center=(WIDTH / 2, HEIGHT / 2))

min_speed = 1
max_speed = 5

speed_x = random.randint(1, 5) * (random.randint(0, 1) * 2 - 1)
speed_y = random.randint(-5, 5)
score = 0

next_speed_increase = 10

def draw():
    screen.blit("background", (0, 0))
    moon.draw()
    screen.draw.text("Score: "+str(score), (90,60), fontsize=100, color="lightblue")

def on_mouse_down(pos):
    global score, min_speed, max_speed, next_speed_increase

    if moon.collidepoint(pos):
        score += 1
        if score == next_speed_increase:
            min_speed += 1
            max_speed += 1
            next_speed_increase += 10
    else:
        score -= 1

def update():
    global speed_x, speed_y

    # Right wall
    if moon.right >= WIDTH:
        speed_x = random.randint(-max_speed, -min_speed)
        speed_y = random.randint(-max_speed, max_speed)

    # top wall
    if moon.top <= 0:
        speed_x = random.randint(-max_speed, max_speed)
        speed_y = random.randint(min_speed, max_speed)

    # Left wall
    if moon.left <= 0:
        speed_x = random.randint(min_speed, max_speed)
        speed_y = random.randint(-max_speed, max_speed)

    # Bottom wall
    if moon.bottom >= HEIGHT:
        speed_x = random.randint(-max_speed, max_speed)
        speed_y = random.randint(-max_speed, -min_speed)

    moon.x += speed_x
    moon.y += speed_y

pgzrun.go()