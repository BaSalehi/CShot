import pygame
import random


SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
PLAYER_SPEED = 5
TARGET_RADIUS = 20

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

class Parent:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color

class Aim(Parent):
    def __init__(self, x, y, color, controls):
        super().__init__(x, y, color)
        self.controls = controls

    def move(self, keys_pressed):
        if keys_pressed[self.controls["left"]]:
            self.x -= PLAYER_SPEED
        if keys_pressed[self.controls["right"]]:
            self.x += PLAYER_SPEED
        if keys_pressed[self.controls["up"]]:
            self.y -= PLAYER_SPEED
        if keys_pressed[self.controls["down"]]:
            self.y += PLAYER_SPEED

        self.x = max(0, min(self.x, SCREEN_WIDTH))
        self.y = max(0, min(self.y, SCREEN_HEIGHT))

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), 5, 2)


class Target(Parent):
    def __init__(self, x, y, color):
        super().__init__(x, y, color)

    def respawn(self):
        self.x = random.randint(50, SCREEN_WIDTH - 50)
        self.y = random.randint(50, SCREEN_HEIGHT // 2)

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), TARGET_RADIUS)

class Game:
    pass                
