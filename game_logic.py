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
    def __init__(self):
        self.aim1 = Aim(200, 500, (0, 0, 255), {"left": pygame.K_a, "right": pygame.K_d, "up": pygame.K_w, "down": pygame.K_s})
        self.aim2 = Aim(600, 500, (0, 255, 0), {"left": pygame.K_LEFT, "right": pygame.K_RIGHT, "up": pygame.K_UP, "down": pygame.K_DOWN})
        self.targets = [Target(random.randint(50, SCREEN_WIDTH - 50), random.randint(50, SCREEN_HEIGHT // 2), (255, 0, 0)) for i in range(3)]
        self.shots = {"player1": [], "player2": []}
        self.running = True

    def start(self):
        clock = pygame.time.Clock()
        while self.running:
            screen.fill((255, 255, 255))
            self.events()
            self.update()
            self.draw()
            pygame.display.flip()
            clock.tick(30)
    
    def events(self):
        keys_pressed = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.shots["player1"].append((self.aim1.x, self.aim1.y))
                if event.key == pygame.K_SPACE:
                    self.shots["player2"].append((self.aim2.x, self.aim2.y))

        self.aim1.move(keys_pressed)
        self.aim2.move(keys_pressed)

    def update(self):
        for player, shots in self.shots.items():
            for shot in shots:
                for target in self.targets:
                    if abs(shot[0] - target.x) <= TARGET_RADIUS and abs(shot[1] - target.y) <= TARGET_RADIUS:
                        target.respawn()

    def draw(self):
        self.aim1.draw(screen)
        self.aim2.draw(screen)
        for target in self.targets:
            target.draw(screen)
        for shot in self.shots["player1"]:
            pygame.draw.circle(screen, (0, 0, 255), shot, 3)
        for shot in self.shots["player2"]:
            pygame.draw.circle(screen, (0, 255, 0), shot, 3)

game = Game()
game.start()            