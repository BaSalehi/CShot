import pygame
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

def show_top_players():
    Base = declarative_base()

    class Winner(Base):
        __tablename__ = 'winners'
        id = Column(Integer, primary_key=True)
        player_name = Column(String(50))
        score = Column(Integer)
        game_date = Column(DateTime, default=datetime.utcnow)

    try:
        engine = create_engine('postgresql+pg8000://postgres:0880450789asnii@localhost/cshot_winners')
        Session = sessionmaker(bind=engine)
        session = Session()

        winners = session.query(Winner).order_by(Winner.score.desc()).limit(3).all()
        
        pygame.init()
        SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Top Players")
        font = pygame.font.Font(None, 32)

        running = True

        while running:
            screen.fill((245, 245, 245))

            title = font.render("Top 3 Players", True, (0, 0, 0))
            screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 20))

            headers = ["Rank", "Player", "Score", "Date"]
            header_x = [50, 200, 350, 500]
            for i, header in enumerate(headers):
                header_text = font.render(header, True, (0, 0, 128))
                screen.blit(header_text, (header_x[i], 80))
                
            y_offset = 120
            for i, winner in enumerate(winners, 1):
                rank_text = font.render(str(i), True, (0, 0, 0))
                name_text = font.render(winner.player_name, True, (0, 0, 0))
                score_text = font.render(str(winner.score), True, (0, 0, 0))
                date_text = font.render(winner.game_date.strftime('%Y-%m-%d'), True, (0, 0, 0))

                screen.blit(rank_text, (header_x[0], y_offset))
                screen.blit(name_text, (header_x[1], y_offset))
                screen.blit(score_text, (header_x[2], y_offset))
                screen.blit(date_text, (header_x[3], y_offset))
                y_offset += 40

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False

            pygame.display.flip()

        pygame.quit()
        session.close()
        
    except Exception as e:
        print(f"Error showing winners: {e}")
        pygame.quit()
        return False
    
    return True

if __name__ == "__main__":
    show_top_players()