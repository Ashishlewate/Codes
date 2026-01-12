import pygame
import math
import sys

# Initialize
pygame.init()
WIDTH, HEIGHT = 1000, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pirate Ship Ocean Simulation")
clock = pygame.time.Clock()

# Colors
OCEAN_BLUE = (20, 80, 160)
WAVE_BLUE = (30, 120, 200)
SHIP_BROWN = (120, 70, 30)
SAIL_WHITE = (230, 230, 230)
SKY = (135, 206, 235)

# Ship settings
ship_x = WIDTH // 2
ship_y = HEIGHT // 2
ship_speed = 2
wave_offset = 0

def draw_waves(offset):
    for x in range(0, WIDTH, 20):
        y = int(HEIGHT/2 + math.sin((x + offset) * 0.02) * 15)
        pygame.draw.circle(screen, WAVE_BLUE, (x, y), 12)

def draw_ship(x, y, offset):
    bob = math.sin(offset * 0.05) * 8

    # Hull
    pygame.draw.ellipse(screen, SHIP_BROWN, (x - 70, y + bob, 140, 40))

    # Mast
    pygame.draw.rect(screen, (90, 50, 20), (x - 5, y - 80 + bob, 10, 80))

    # Sail
    pygame.draw.polygon(
        screen,
        SAIL_WHITE,
        [(x, y - 80 + bob), (x + 60, y - 30 + bob), (x, y - 30 + bob)]
    )

running = True
while running:
    clock.tick(60)
    screen.fill(SKY)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Ocean
    pygame.draw.rect(screen, OCEAN_BLUE, (0, HEIGHT/2, WIDTH, HEIGHT/2))
    draw_waves(wave_offset)

    # Move ship
    ship_x += ship_speed
    if ship_x > WIDTH + 100:
        ship_x = -100

    draw_ship(ship_x, ship_y, wave_offset)

    wave_offset += 2
    pygame.display.flip()

pygame.quit()
sys.exit()
