import pygame
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

Base = declarative_base()

class Winner(Base):
    __tablename__ = 'winners'
    id = Column(Integer, primary_key=True)
    player_name = Column(String(50))
    score = Column(Integer)
    game_date = Column(DateTime, default=datetime.utcnow)


engine = create_engine('postgresql+pg8000://postgres:0880450789asnii@localhost/cshot_winners')
Session = sessionmaker(bind=engine)
session = Session()

winners = session.query(Winner).order_by(Winner.score.desc()).all()

print("**winners**")
for winner in winners:
    print(f"{winner.player_name} - Score: {winner.score} - Date: {winner.game_date.strftime('%Y-%m-%d %H:%M:%S')}")

session.close()

pygame.init()
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Winners Chart")
font = pygame.font.Font(None, 32)

running = True

while running:
    screen.fill((245, 245, 245))

    
    title = font.render("**Winners**", True, (0, 0, 0))
    screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 20))

    
    headers = ["Player", "Score", "Date"]
    header_x = [100, 300, 500]
    for i, header in enumerate(headers):
        header_text = font.render(header, True, (0, 0, 128))
        screen.blit(header_text, (header_x[i], 80))

    # data
    y_offset = 120
    for winner in winners:
        name_text = font.render(winner.player_name, True, (0, 0, 0))
        score_text = font.render(str(winner.score), True, (0, 0, 0))
        date_text = font.render(winner.game_date.strftime('%Y-%m-%d'), True, (0, 0, 0))

        screen.blit(name_text, (header_x[0], y_offset))
        screen.blit(score_text, (header_x[1], y_offset))
        screen.blit(date_text, (header_x[2], y_offset))
        y_offset += 40

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()

pygame.quit()