import pygame
import random
import time
import math

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
PLAYER_SPEED = 5
TARGET_RADIUS = 20
TIME_LIMIT = 100

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
        self.scores={"player1": 0, "player2": 0}
        self.start_time=time.time()
        self.running = True
        self.font= pygame.font.Font(None,36)

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
        elapsed_time=int(time.time()- self.start_time)
        self.time_remaining= max(0,TIME_LIMIT - elapsed_time)

        if self.time_remaining==0:
            self.running=False
            self.show_winner()
        
        for player in ["player1", "player2"]:
            if len(self.shots[player]) < 2:  
                continue  

            last_shot = self.shots[player][-2]  
            current_shot = self.shots[player][-1]  
            for target in self.targets:  
                distance = math.dist(current_shot, (target.x, target.y)) 

                if distance <= TARGET_RADIUS:  
                    shot_distance = math.dist(last_shot, current_shot)  
                
                    if shot_distance < 30:
                        score = 1
                    elif shot_distance < 80:
                        score = 2
                    elif shot_distance < 150:
                        score = 3
                    elif shot_distance < 250:
                        score = 4
                    else:
                        score = 5
                    self.scores[player] += score  
                    target.respawn()  
                    print(shot_distance)
                    break

    def draw(self):
        self.aim1.draw(screen)
        self.aim2.draw(screen)
        for target in self.targets:
            target.draw(screen)
        for shot in self.shots["player1"]:
            pygame.draw.circle(screen, (0, 0, 255), shot, 3)
        for shot in self.shots["player2"]:
            pygame.draw.circle(screen, (0, 255, 0), shot, 3)

        score_text = f"player 1: {self.scores['player1']} | player 2: {self.scores['player2']} | Time: {self.time_remaining}s"
        text_surface = self.font.render(score_text, True, (0,0,0))
        screen.blit(text_surface, (20, 10)) 

    def show_winner(self):
        screen.fill((255,255,255))
        winner_text="Game Over!"
        if self.scores["player1"]>self.scores["player2"]:
            winner_text +="Player 1 Won!"
        elif self.scores["player1"]<self.scores["player2"]:
            winner_text+="Player 2 Won!" 
        else:
            winner_text+="It's a Tie!"   

        text_surface= self.font.render(winner_text, True, (255,0,0))
        screen.blit(text_surface, (SCREEN_WIDTH//2 - 100 , SCREEN_HEIGHT//2))  
        pygame.display.flip()
        pygame.time.delay(5000)
        pygame.quit() 

game = Game()
game.start()            