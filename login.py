import pygame
import json 
import os
import sys

# Initialize Pygame
pygame.init()

# Colors
DARK_RED = (139, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

# Fonts
FONT = pygame.font.Font(None, 32)
ERROR_FONT = pygame.font.Font(None, 24)

class DataSaving:
    def __init__(self, user1, user2):
        self.user1 = user1
        self.user2 = user2
        self.users = {'user1': user1,
                      'user2': user2}
        
    # saves the given usernames in a json file
    def SaveInJon(self):
        if os.path.exists('users.json'):
            with open('users.json', 'r') as file:
                new_users = json.load(file)
        new_users.append(self.users)

        try:
            with open('users.json', 'w') as file:
                json.dump(new_users, file, indent=4)
        except Exception as e:
            print(f"An error occurred while writing to the file: {e}")
            
class InputBox:
    def __init__(self, x, y, width, height, label):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = GRAY
        self.text = ''
        self.label = label
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = WHITE if self.active else GRAY  # Changed to white when active

        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
                print(f"{self.label}: {self.text}")
                self.text = ''
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                self.text += event.unicode

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, 2)

        # Render the text in white
        txt_surface = FONT.render(self.text, True, WHITE)  # Changed to white text
        screen.blit(txt_surface, (self.rect.x + 5, self.rect.y + 5))

        # Render the label in white
        label_surface = FONT.render(self.label, True, WHITE)  # Changed to white
        screen.blit(label_surface, (self.rect.x - 100, self.rect.y + 5))


class Button:
    def __init__(self, x, y, width, height, text, color=BLACK):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
    
    # continue button
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        txt_surface = FONT.render(self.text, True, WHITE)
        screen.blit(txt_surface, (self.rect.x + 10, self.rect.y + 10))

    # check if the continue button is pressed 
    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True
        return False
    
class LoginPage:
    def __init__(self, width, height):
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Login Page")
        self.clock = pygame.time.Clock()
        self.input_box1 = InputBox(300, 200, 200, 32, "User 1:")
        self.input_box2 = InputBox(300, 300, 200, 32, "User 2:")
        self.continue_button = Button(300, 400, 200, 50, "Continue")
        self.running = True
        self.error_message = ""
        self.new_users = []

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                    sys.exit()

                self.input_box1.handle_event(event)
                self.input_box2.handle_event(event)

                if self.continue_button.is_clicked(event):
                    if self.validate_usernames():
                        self.save_usernames()
                        self.running = False
                    else:
                        #redraw page to show the error message if theres any
                        self.screen.fill(DARK_RED)
                        self.input_box1.draw(self.screen)
                        self.input_box2.draw(self.screen)
                        self.continue_button.draw(self.screen)
                        error_surface = ERROR_FONT.render(self.error_message, True, WHITE)  # Changed to white
                        self.screen.blit(error_surface, (300, 460))  # Adjusted position
                        pygame.display.flip()

            self.screen.fill(DARK_RED)
            self.input_box1.draw(self.screen)
            self.input_box2.draw(self.screen)
            self.continue_button.draw(self.screen)
            
            # write error message if exists
            if self.error_message:
                error_surface = ERROR_FONT.render(self.error_message, True, WHITE) 
                self.screen.blit(error_surface, (300, 460))

            pygame.display.flip()
            self.clock.tick(30)

    def validate_usernames(self):
        #check for empty strings
        user1 = self.input_box1.text.strip()
        user2 = self.input_box2.text.strip()
        
        if not user1 or not user2:
            self.error_message = "Usernames cannot be empty!"
            return False
        self.error_message = ""
        return True
    
    # save the users in the json file
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

if __name__ == "__main__":
    login_page = LoginPage(800, 600)
    login_page.run()