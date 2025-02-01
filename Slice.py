import math

import pygame
import pygame.gfxdraw


class Slice:
    def __init__(self, window, center, points: list, radius, name: str, color: tuple or pygame.Color):
        self.parent = window
        self.center = center
        self.points = points
        self.color = pygame.Color(color)
        if (self.color.r * 0.299 + self.color.g * 0.587 + self.color.b * 0.114) > 186:
            self.text_color = pygame.Color('#000000')
        else:
            self.text_color = pygame.Color('#ffffff')
        self.radius = radius

        self.name = name
        self.font = pygame.font.SysFont('Sans', 20, 1)

    def new_arc(self, points: list):
        new_points = points.copy()
        new_points.append(self.center)
        self.points = new_points

    def draw(self):
        black = (0, 0, 0)
        points = self.points.copy()
        points.append(self.center)

        pygame.gfxdraw.filled_polygon(self.parent, points, self.color)
        pygame.draw.aaline(self.parent, black, self.center, self.points[0])
        pygame.draw.aaline(self.parent, black, self.center, self.points[1])

        angle_point = ((self.points[-2][0] + self.points[0][0]) / 2,
                       (self.points[-2][1] + self.points[0][1]) / 2)
        angle = math.atan2(self.center[1] - angle_point[1], angle_point[0] - self.center[0])

        if angle < - math.pi / 2 or angle > math.pi / 2:
            angle -= math.pi

        text = self.font.render(self.name, 1, self.text_color)
        text = pygame.transform.rotate(text, math.degrees(angle))
        middle_point = ((angle_point[0] + self.center[0]) / 2, (angle_point[1] + self.center[1]) / 2)
        text_rect = text.get_rect(center=middle_point)

        self.parent.blit(text, text_rect)
