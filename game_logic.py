import pygame
import random
import time
import math
clock=pygame.time.Clock()

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
PLAYER_SPEED = 5
TARGET_RADIUS = 20
TIME_LIMIT = 100

pygame.init()
display = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

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

    def respawn(self, existing_targets):
        self.x, self.y = Target.safe_respawn(existing_targets)

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), TARGET_RADIUS)

    @staticmethod
    def safe_respawn(existing_targets, radius=TARGET_RADIUS):
        while True:
            x = random.randint(50, SCREEN_WIDTH - 50)
            y = random.randint(50, SCREEN_HEIGHT // 2)    
            overlap = False
            for target in existing_targets:
                dist = math.dist((x, y), (target.x, target.y))
                if dist < radius * 2 + 10:
                    overlap = True
                    break
            if not overlap:
                return x, y 

#adds score and time
class silver_target_item(Target):
    def __init__(self, x, y, color, time_bonus=5):
        super().__init__(x, y, color)
        self.time_bonus=time_bonus

# subs time
class black_target_item(Target):
    def __init__(self, x, y, color, time_penalty = 5):
        super().__init__(x, y, color)
        self.time_penalty = time_penalty
        self.vx = random.choice([-3, 3])
    def move(self):
        self.x += self.vx
        if self.x <= TARGET_RADIUS or self.x >= SCREEN_WIDTH - TARGET_RADIUS:
            self.vx *= -1 

# shows the aim
class bronze_target_item(Target):
    def __init__(self, x, y, color=(205, 127, 50)):
        super().__init__(x, y, color)

# adds bullet
class gold_target_item(Target):
    def __init(self, x, y, color=(255, 215, 0)):
        super().__init__(x, y, color)

class Game:
    def __init__(self, user1, user2):
        pygame.init()
        pygame.mixer.init()
        
        self.start_game_sound = pygame.mixer.Sound("start-game-sound.wav")
        self.shot_sound = pygame.mixer.Sound("shot-sound.wav")
        self.end_game_sound = pygame.mixer.Sound("end-game-sound.wav") 
        
        self.start_game_sound.play()

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.aim1 = Aim(200, 500, (139, 0, 0), {"left": pygame.K_a, "right": pygame.K_d, "up": pygame.K_w, "down": pygame.K_s})
        self.aim2 = Aim(600, 500, (139, 0, 0), {"left": pygame.K_LEFT, "right": pygame.K_RIGHT, "up": pygame.K_UP, "down": pygame.K_DOWN})
        # self.targets = [Target(random.randint(50, SCREEN_WIDTH - 50), random.randint(50, SCREEN_HEIGHT // 2), (34, 139, 34)) for i in range(3)] 
        # self.targets.append(silver_target_item(random.randint(50, SCREEN_WIDTH - 50), random.randint(5, SCREEN_HEIGHT//2), (192,192,192)))
        self.targets = []
        for i in range(3):
            x, y = Target.safe_respawn(self.targets)
            self.targets.append(Target(x, y, (255, 0, 0)))
        self.shots = {user1: [], user2: []}
        
        self.silver_target = None
        self.silver_spawn_time_out = 20000
        self.silver_spawn_time_in = 15000
        self.silver_visible_since = None
        self.last_silver_spawn_time = pygame.time.get_ticks()

        self.user1 = user1
        self.user2 = user2
        self.scores={user1: 0, user2: 0}
        self.time_remaining={self.user1: 100, self.user2: 100}

        self.last_update_time=pygame.time.get_ticks()
        self.start_time=time.time()
        self.running = True
        self.font= pygame.font.Font(None,36)

        self.black_target= None
        self.black_visible_since = None
        self.last_black_spawn_time = pygame.time.get_ticks()
        self.black_target_time_out = 20000
        self.black_target_time_in = 15000
        # self.black_target = black_target_item(random.randint(50, SCREEN_WIDTH - 50), random.randint(50, SCREEN_HEIGHT // 2), (0, 0, 0)) 

        self.bullets = {self.user1: 10, self.user2: 10}

        self.bronze_target = None
        self.last_bronze_spawn_time = pygame.time.get_ticks()
        self.bronze_item_time_in = 15000
        self.bronze_target_time_out = 20000 

        self.gold_target = None
        self.last_gold_spawn_time = pygame.time.get_ticks()
        self.gold_target_time_out = 15000  
        self.gold_target_time_in = 20000 

        self.aim_visible_until = {self.user1: 0, self.user2: 0}
        self.previous_shot_hit = {self.user1: False, self.user2: False}

    def start(self):
        clock = pygame.time.Clock()
        while self.running:
            self.screen.fill((139, 0, 0)) 
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
                if event.key == pygame.K_SPACE and self.bullets[self.user1] > 0:
                    self.shots[self.user1].append((self.aim1.x, self.aim1.y))
                    self.bullets[self.user1] -= 1
                    self.shot_sound.play()
                if event.key == pygame.K_RETURN and self.bullets[self.user2] > 0:
                    self.shots[self.user2].append((self.aim2.x, self.aim2.y))
                    self.bullets[self.user2] -= 1
                    self.shot_sound.play()

        self.aim1.move(keys_pressed)
        self.aim2.move(keys_pressed)

    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_update_time >= 1000:  
            for player in [self.user1, self.user2]:
                self.time_remaining[player] = max(0, self.time_remaining[player] - 1)  
            self.last_update_time = current_time  

            if self.time_remaining[player]==0:
                self.running=False
                self.show_winner()

        if self.bullets[self.user1] == 0 and self.bullets[self.user2] == 0:
            self.running = False
            self.show_winner()
            return 
        
        if self.black_target is None and (current_time - self.last_black_spawn_time >= 25000):
            # self.black_target = black_target_item(random.randint(50, SCREEN_WIDTH - 50), random.randint(50, SCREEN_HEIGHT//2), (0,0,0))
            x, y = Target.safe_respawn(self.targets + ([self.silver_target] if self.silver_target else []))
            self.black_target = black_target_item(x, y, (0, 0, 0))
            self.black_visible_since = current_time 
        
        if self.black_target  and (current_time - self.black_visible_since >= 15000):
            self.black_target = None
            self.last_black_spawn_time = current_time 

        if self.silver_target is None and (current_time - self.last_silver_spawn_time >= 20000):
            # self.silver_target = silver_target_item(random.randint(50, SCREEN_WIDTH - 50), random.randint(50, SCREEN_HEIGHT // 2), (192, 192, 192))
            x, y = Target.safe_respawn(self.targets + ([self.black_target] if self.black_target else []))
            self.silver_target = silver_target_item(x, y, (192, 192, 192))     
            # self.silver_spawn_time_out = current_time
            self.silver_visible_since = current_time
        
        if self.silver_target and ( current_time - self.silver_visible_since >= 15000):
            self.silver_target = None
            self.last_silver_spawn_time = current_time

        if self.bronze_target is None and (current_time - self.last_bronze_spawn_time >= 20000):
            x, y = Target.safe_respawn(self.targets + ([self.black_target] if self.black_target else []) + ([self.silver_target] if self.silver_target else []))
            self.bronze_target = bronze_target_item(x, y, (205, 127, 50))
            self.bronze_visible_since = current_time

        if self.bronze_target and (current_time - self.bronze_visible_since >= 15000):
            self.bronze_target = None
            self.last_bronze_spawn_time = current_time 

        if self.gold_target is None and (current_time - self.last_gold_spawn_time >= 30000):
            x, y = Target.safe_respawn(self.targets + ([self.silver_target] if self.silver_target else []) + ([self.black_target] if self.black_target else []) + ([self.bronze_target] if self.bronze_target else []))
            self.gold_target = gold_target_item(x, y, (255, 215, 0))
            self.gold_visible_since = current_time

        if self.gold_target and (current_time - self.gold_visible_since >= 10000):
            self.gold_target = None
            self.last_gold_spawn_time = current_time  

        for player in [self.user1, self.user2]:
            if len(self.shots[player]) < 2:  
                continue  

            last_shot = self.shots[player][-2]  
            current_shot = self.shots[player][-1]  

            for target in self.targets:  
                distance = math.dist(current_shot, (target.x, target.y)) 

                if distance <= TARGET_RADIUS:  
                    shot_distance = math.dist(last_shot, current_shot)  
                    if isinstance(target, silver_target_item):
                        self.time_remaining[player] = min(300, self.time_remaining[player] + 10)    
                    
                    if shot_distance < 50:
                        score = 1
                    elif shot_distance < 100:
                        score = 2
                    elif shot_distance < 150:
                        score = 3
                    elif shot_distance < 250:
                        score = 4
                    else:
                        score = 5

                    self.scores[player] += score  
                    target.respawn(self.targets)  
                    print(shot_distance)
                    break  

        if self.black_target:
            self.black_target.move()

            for player in [self.user1, self.user2]:
                distance_aim = math.dist((self.aim1.x, self.aim1.y) if player == self.user1 else (self.aim2.x, self.aim2.y), (self.black_target.x, self.black_target.y))
                if distance_aim <= TARGET_RADIUS:
                    self.time_remaining[player] = max(0, self.time_remaining[player] - self.black_target.time_penalty)
                    self.black_target = None
                    self.last_black_spawn_time = current_time

        for player in [self.user1, self.user2]:
            if self.silver_target:
                distance_aim = math.dist((self.aim1.x, self.aim1.y) if player == self.user1 else (self.aim2.x, self.aim2.y),(self.silver_target.x, self.silver_target.y))
                if distance_aim <= TARGET_RADIUS:
                    self.time_remaining[player] = min(100, self.time_remaining[player] + 10)
                    self.silver_target = None
                    self.last_silver_spawn_time = current_time

        for player in [self.user1, self.user2]:
            if self.bronze_target:
                distance_aim = math.dist((self.aim1.x, self.aim1.y) if player == self.user1 else (self.aim2.x, self.aim2.y), (self.bronze_target.x, self.bronze_target.y))
                if distance_aim <= TARGET_RADIUS:
                    self.aim_visible_until[player] = current_time + 10000 
                    self.bronze_target = None
                    self.last_bronze_spawn_time = current_time            

        for player in [self.user1, self.user2]:
            if self.gold_target:
                distance_aim = math.dist((self.aim1.x, self.aim1.y) if player == self.user1 else (self.aim2.x, self.aim2.y), (self.gold_target.x, self.gold_target.y))
                if distance_aim <= TARGET_RADIUS:
                    self.bullets[player] = min(30, self.bullets[player] + 5) 
                    self.gold_target = None
                    self.last_gold_spawn_time = current_time             

    def draw(self):
        self.aim1.draw(self.screen)
        self.aim2.draw(self.screen)

        current_time = pygame.time.get_ticks()
        if current_time < self.aim_visible_until[self.user1]:
            GraphicsHelper.draw_crosshair(self.screen, (self.aim1.x, self.aim1.y), color=(0, 0, 255))
        if current_time < self.aim_visible_until[self.user2]:
            GraphicsHelper.draw_crosshair(self.screen, (self.aim2.x, self.aim2.y), color=(0, 255, 0))

        for target in self.targets:
            target.draw(self.screen)
        for shot in self.shots[self.user1]:
            pygame.draw.circle(self.screen, (0, 0, 255), shot, 3)
        for shot in self.shots[self.user2]:
            pygame.draw.circle(self.screen, (0, 255, 0), shot, 3)

        if self.black_target:
            self.black_target.draw(self.screen)    
        if self.bronze_target:
            self.bronze_target.draw(self.screen)
        if self.silver_target:
            self.silver_target.draw(self.screen) 
        if self.gold_target:
            self.gold_target.draw(self.screen)

        font=pygame.font.Font(None, 36)    
        text_p1 = font.render(f"{self.user1} - Score: {self.scores[self.user1]}  Time: {self.time_remaining[self.user1]} Bullets: {self.bullets[self.user1]}", True, (0, 0, 255))
        text_p2 = font.render(f"{self.user2} - Score: {self.scores[self.user2]}  Time: {self.time_remaining[self.user2]} Bullets: {self.bullets[self.user2]}", True, (0, 255, 0))

        self.screen.blit(text_p1, (20, 10))
        self.screen.blit(text_p2, (20, 50)) 
    def show_winner(self):
        self.end_game_sound.play()
        self.screen.fill((255,255,255))
        winner_text="Game Over! "
        if self.scores[self.user1]>self.scores[self.user2]:
            winner_text += f"{self.user1} Won!"
        elif self.scores[self.user1]<self.scores[self.user2]:
            winner_text+= f"{self.user2} Won!" 
        else:
            winner_text+="It's a Tie!"   

        text_surface= self.font.render(winner_text, True, (255,0,0))
        self.screen.blit(text_surface, (SCREEN_WIDTH//2 - 100 , SCREEN_HEIGHT//2))  
        pygame.display.flip()
        pygame.time.delay(5000)
        pygame.quit() 

class GraphicsHelper:
    @staticmethod
    def draw_crosshair(surface, position, color=(0, 0, 0)):
        pygame.draw.line(surface, color, (position[0] - 10, position[1]), (position[0] + 10, position[1]), 2)
        pygame.draw.line(surface, color, (position[0], position[1] - 10), (position[0], position[1] + 10), 2)        

if __name__ == "__main__": 
    game = Game()
    game.start()