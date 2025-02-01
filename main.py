import math
import random

import pygame
import pygame.gfxdraw
from Wheel import Wheel


def draw_indicator(window, center, radius):
    pygame.gfxdraw.filled_trigon(
        window,
        center[0], center[1] - radius + 15,
        center[0] - 15, center[1] - radius - 30,
        center[0] + 15, center[1] - radius - 30,
        (255, 0, 0)
    )


def main():
    pygame.init()
    pygame.font.init()

    font = pygame.font.SysFont('Comic Sans MS', 30)
    # logo = pygame.image.load('logo32x32.png')
    # pygame.display.set_icon(logo)
    pygame.display.set_caption('Wheel Of Fortune')
    window = pygame.display.set_mode((1920, 1080))
    window.fill((0, 0, 0))

    radius = 530
    center = (1920 // 2, 1080 // 2)

    with open('fields.txt', encoding='UTF8') as reader:
        fields = [line.strip() for line in reader]
    with open('colours.txt', encoding='UTF8') as reader:
        colours = [line.strip() for line in reader]

    wheel = Wheel(window, center, radius, fields, colours)

    angle = 0
    velocity = 0
    acceleration = -0.2
    clock = pygame.time.Clock()
    running = True
    start_time = None
    while running:
        window.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_SPACE:
                    velocity += math.fabs(random.gauss(10, 3))
            if event.type == pygame.MOUSEBUTTONDOWN:
                start_time = pygame.time.get_ticks()
            if event.type == pygame.MOUSEBUTTONUP:
                if start_time is not None:
                    click_time = pygame.time.get_ticks() - start_time
                    velocity += math.fabs(random.gauss(click_time / 10, click_time / 100))
                    start_time = None
            elif event.type == pygame.QUIT:
                running = False
        wheel.draw(angle)
        draw_indicator(window, center, radius)

        if velocity > 0:
            velocity = velocity + acceleration

        else:
            velocity = 0.
            winner = wheel.find_closest((center[0], center[1] - radius + 15))

            text_surface = font.render(f'{winner}', True, (255, 255, 255))

            pygame.transform.rotate(text_surface, angle)
            window.blit(text_surface, (50, 50))
        angle = (angle + velocity) % wheel.no_points
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
