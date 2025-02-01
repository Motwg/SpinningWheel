import math
import random

import pygame

from Slice import Slice
from utils import distance


class Wheel:
    def __init__(self, window, center, radius, fields: list, palette: list):
        self.parent = window
        self.center = center
        self.radius = radius
        self.no_slices = len(fields)
        self.no_points_per_slice = 5_000 // len(fields)
        self.no_points = self.no_slices * self.no_points_per_slice
        points = [(math.sin(math.radians(360 / self.no_points * i)) * radius + center[0],
                   math.cos(math.radians(360 / self.no_points * i)) * radius + center[1])
                  for i in range(self.no_points)]
        points.extend(points[:self.no_points_per_slice])
        self.points = points

        try:
            palette = [pygame.Color(colour) for colour in palette]
        except ValueError:
            palette = [pygame.Color(colour) for colour in ['#84dcc6',
                                                           '#d6edff',
                                                           '#acd7ec',
                                                           '#8b95c9',
                                                           '#478978']]

        colours = [random.choice(palette)]
        for i in range(len(fields) - 2):
            colour = random.choice(palette)
            while colour == colours[i]:
                colour = random.choice(palette)
            colours.append(colour)
        colour = random.choice(palette)
        while colour == colours[0] or colour == colours[-1]:
            colour = random.choice(palette)
        colours.append(colour)

        self.slices = [Slice(self.parent, self.center, [], self.radius, field,
                             colour) for field, colour in zip(fields, colours)]

    def draw(self, angle_offset):
        for i, piece in enumerate(self.slices):
            start_index = i * self.no_points_per_slice + int(angle_offset % self.no_points)
            piece.new_arc(
                self.points[start_index % self.no_points: start_index % self.no_points + self.no_points_per_slice]
            )
            piece.draw()
        pygame.draw.circle(self.parent, (255, 255, 255), self.center, self.radius, 1)
        pygame.draw.circle(self.parent, (255, 255, 255), self.center, 10)

    def find_closest(self, point) -> str:
        nearest_point = ('None', float('inf'))
        for piece in self.slices:
            if (x1 := distance(piece.points[0], point)) < nearest_point[1]:
                nearest_point = piece.name, x1
            if (x2 := distance(piece.points[-2], point)) < nearest_point[1]:
                nearest_point = piece.name, x2
        return nearest_point[0]
