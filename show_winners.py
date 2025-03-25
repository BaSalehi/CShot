import pygame
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

# color constants
DARK_RED = (139, 0, 0)
BLACK = (0, 0, 0)
BLUE_HEADER = (0, 0, 128)

# function to display the top 3 players from the database
def show_top_players(screen, font, clock):
    #sqlalchemy setup for saving game winners
    Base = declarative_base()

    class Winner(Base):
        __tablename__ = 'winners'
        id = Column(Integer, primary_key=True)
        player_name = Column(String(50))
        score = Column(Integer)
        game_date = Column(DateTime, default=datetime.utcnow)

    try:
        #Connect to the PostgreSQL database
        engine = create_engine('postgresql+pg8000://postgres:0880450789asnii@localhost/cshot_winners')
        Session = sessionmaker(bind=engine)
        session = Session()

        #query the top 3 players by highest score
        winners = session.query(Winner).order_by(Winner.score.desc()).limit(3).all()
        
        # Pygame window for showing the leaderboard
        pygame.init()
        SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Top Players")
        font = pygame.font.Font(None, 32)
        title_font = pygame.font.Font(None, 48)

        running = True

        # main loop for displaying the top 3 players
        while running:
            screen.fill(DARK_RED)

            title = font.render("Top 3 Players", True, BLACK)
            screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 20))

            # draw headers for Rank, Player Name, Score, and Date
            headers = ["Rank", "Player", "Score", "Date"]
            header_x = [50, 200, 350, 500]
            for i, header in enumerate(headers):
                header_text = font.render(header, True, BLUE_HEADER)
                screen.blit(header_text, (header_x[i], 100))

            #display each player's data in rows
            y_offset = 120
            for i, winner in enumerate(winners, 1):
                rank_text = font.render(str(i), True, BLACK)
                name_text = font.render(winner.player_name, True, BLACK)
                score_text = font.render(str(winner.score), True, BLACK)
                date_text = font.render(winner.game_date.strftime('%Y-%m-%d'), True, BLACK)

                screen.blit(rank_text, (header_x[0], y_offset))
                screen.blit(name_text, (header_x[1], y_offset))
                screen.blit(score_text, (header_x[2], y_offset))
                screen.blit(date_text, (header_x[3], y_offset))
                y_offset += 50

            #display a hint at the bottom for how to exit
            hint_font = pygame.font.Font(None, 24)
            hint_text = hint_font.render("Press ESC or close window to return", True, BLACK)
            screen.blit(hint_text, (SCREEN_WIDTH//2 - hint_text.get_width()//2, SCREEN_HEIGHT - 40))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return True

            pygame.display.flip()
            clock.tick(30)

        # close the database session after use
        session.close()
        return True
    
    except Exception as e:
        #print any errors that occur
        print(f"Error showing top 3 players: {e}")
        return True
    
# If the script is run directly, initialize pygame and show top players
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    font = pygame.font.Font(None, 32)
    clock = pygame.time.Clock()
    show_top_players(screen, font, clock)
    pygame.quit()