import pygame
import json 
import os
import sys
from game_logic import Game, SCREEN_WIDTH, SCREEN_HEIGHT 
from show_winners import show_top_players

# Colors
DARK_RED = (139, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

# Fonts
FONT = pygame.font.Font(None, 32)
ERROR_FONT = pygame.font.Font(None, 24)

# input box class
class InputBox:
    def __init__(self, x, y, width, height, label, click_sound):
        # initialize input box properties
        self.rect = pygame.Rect(x, y, width, height)
        self.color = GRAY
        self.text = ''
        self.label = label
        self.active = False
        self.click_sound = click_sound

    def handle_event(self, event):
        # activate mode if input box is clicked on
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
                self.click_sound.play()
            else:
                self.active = False

            # change input box color if activated
            self.color = WHITE if self.active else GRAY

        # handle keyboard input when active
        if event.type == pygame.KEYDOWN and self.active:
            # submit if enter button is pressed
            if event.key == pygame.K_RETURN:
                print(f"{self.label}: {self.text}")
                self.text = ''
            # delete if backspace button is pressed
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            # add characters
            else:
                self.text += event.unicode

    # render the input box on screen
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, 2)
        txt_surface = FONT.render(self.text, True, WHITE)
        screen.blit(txt_surface, (self.rect.x + 5, self.rect.y + 5))
        label_surface = FONT.render(self.label, True, WHITE)
        screen.blit(label_surface, (self.rect.x - 100, self.rect.y + 5))

# button class
class Button:
    # initialize button properties
    def __init__(self, x, y, width, height, text, click_sound, color=BLACK):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.click_sound = click_sound

    # render the button on screen
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        txt_surface = FONT.render(self.text, True, WHITE)
        screen.blit(txt_surface, (self.rect.x + 10, self.rect.y + 10))

    # check if the button is clicked
    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.click_sound.play()
                return True
        return False
    
# login page class
class LoginPage:
    def __init__(self, width, height):
        # initialize pygame and sound player
        pygame.init()
        pygame.mixer.init()

        # window setup
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Login Page")

        # sound effects
        self.click_sound = pygame.mixer.Sound("click-sound.wav")
        self.start_login_sound = pygame.mixer.Sound("start-login-sound.wav")
        self.start_login_sound.play()

        # visual properties
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 32)
        self.input_box1 = InputBox(300, 200, 200, 32, "User 1:", self.click_sound)
        self.input_box2 = InputBox(300, 300, 200, 32, "User 2:", self.click_sound)
        self.continue_button = Button(300, 400, 200, 50, "Continue", self.click_sound)
        self.top_players_button = Button(300, 470, 200, 50, "Top Players", self.click_sound, (70, 70, 70))

        # state variables
        self.running = True
        self.error_message = ""
        self.new_users = []

    # main application loop
    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    break

                # handle input box events
                self.input_box1.handle_event(event)
                self.input_box2.handle_event(event)

                # handle continue button events
                if self.continue_button.is_clicked(event):
                    self.click_sound.play()
                    if self.validate_usernames():
                        self.save_usernames()
                        self.running = False  
                        self.start_game()
                        # retstart after game ends
                        self.__init__(800, 600)
                        self.running = True
                    else:
                        self.show_error()

                # handle top players button events
                if self.top_players_button.is_clicked(event):
                    self.click_sound.play()
                    if not show_top_players(self.screen, self.font, self.clock):
                        self.running = False
                        break
                    
                    # redraw login page after returning
                    self.screen.fill(DARK_RED)
                    self.input_box1.draw(self.screen)
                    self.input_box2.draw(self.screen)
                    self.continue_button.draw(self.screen)
                    self.top_players_button.draw(self.screen)

                    if self.error_message:
                        error_surface = ERROR_FONT.render(self.error_message, True, WHITE)
                        self.screen.blit(error_surface, (300, 540))
                    pygame.display.flip()

            # exit if quit button is pressed
            if not self.running:
                break

            # draw the main login page
            self.screen.fill(DARK_RED)
            self.input_box1.draw(self.screen)
            self.input_box2.draw(self.screen)
            self.continue_button.draw(self.screen)
            self.top_players_button.draw(self.screen)

            if self.error_message:
                error_surface = ERROR_FONT.render(self.error_message, True, WHITE)
                self.screen.blit(error_surface, (300, 540))

            pygame.display.flip()
            self.clock.tick(30)
        
        pygame.quit()
    
    # display error message
    def show_error(self):
        self.screen.fill(DARK_RED)
        self.input_box1.draw(self.screen)
        self.input_box2.draw(self.screen)
        self.continue_button.draw(self.screen)
        error_surface = ERROR_FONT.render(self.error_message, True, WHITE)
        self.screen.blit(error_surface, (300, 460))
        pygame.display.flip()

    # checks if usernames are empty or not
    def validate_usernames(self):
        global user1
        global user2
        user1 = self.input_box1.text.strip()
        user2 = self.input_box2.text.strip()
        
        if not user1 or not user2:
            self.error_message = "Usernames cannot be empty!"
            return False
        self.error_message = ""
        return True
    
    # saves the usernames in a json file
    def save_usernames(self):
        user1 = self.input_box1.text.strip()
        user2 = self.input_box2.text.strip()
        
        self.users = {'user1': user1, 'user2': user2}
        if os.path.exists('users.json'):
            with open('users.json', 'r') as file:
                self.new_users = json.load(file)
        else:
            self.new_users = []
            
        self.new_users.append(self.users)
        
        try:
            with open('users.json', 'w') as file:
                json.dump(self.new_users, file, indent=4)
        except Exception as e:
            print(f"Error saving data: {e}")

    def start_game(self):
        # close the login window 
        pygame.quit()
        # initialize the new game window
        pygame.init()
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

        # start the game with the given users
        game = Game(user1, user2)
        game.start()

if __name__ == "__main__":
    login_page = LoginPage(800, 600)
    login_page.run()