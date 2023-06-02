from flask import Flask, request, jsonify
from flask_cors import CORS
from PIL import Image
from io import BytesIO
import os
import base64
import time
import random
import time
import sys,pygame
from pygame.locals import *
pygame.init()
pygame.font.init()



# Read the allowed origin from the environment variable
allowed_origin = os.environ.get("ALLOWED_ORIGIN", "http://localhost")

app = Flask(__name__)
if os.environ.get("DEBUG").lower() == 'true':
    app.debug = True

CORS(app, resources={r"/*": {"origins": allowed_origin}})


@app.route('/game', methods=['POST'])
def game():
    width = 800
    height = 800
    tempo = 1
    font = pygame.font.Font('freesansbold.ttf', 32)
    white = (255, 255, 255)
    green = (0, 255, 0)
    blue = (0, 0, 128)
    score = 0
    score_increment = 1
    font = pygame.font.Font(None, 36)
    #text = font.render('Game Over!', True, green, blue)
    #gettext = text.get_rect()
    size = width, height
    lane = int(width/2)
    line = int(width/100)
    leftside = width/2 - lane/4
    rightside= width/2 + lane/4

    pygame.init()
    running = True
    screen = pygame.display.set_mode((size))
    pygame.display.set_caption("Courage Game")
    screen.fill((51,255,153))

    pygame.display.update()

    hero = pygame.image.load("mark1.png")
    hero_locat = hero.get_rect()
    hero_locat.center = rightside, height*0.7

    bully = pygame.image.load("bully.png")
    bully_locat = bully.get_rect()
    bully_locat.center = leftside, height*0.1
    count = 1 
    while running:
        bully_locat[1] += tempo
        count +=1
        if count == 300:
            tempo += 0.2
            count = 0
            print("Next Level", tempo)
        if bully_locat[1] > height:
            if random.randint(0,1) == 0:
                bully_locat.center =rightside, -100
                score += score_increment
            else:
                bully_locat.center =leftside, -100
                score += score_increment
            
        if (hero_locat [0] == bully_locat[0]) and (bully_locat [1] > hero_locat [1] - 70):
            #screen.blit(text, gettext)
            score_text = font.render(f'Game Over! Score: {score}', True, green, blue)
            screen.blit(score_text, (10, 10))
            pygame.display.update()
            time.sleep(5)
            break
        
            

        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            if event.type == KEYDOWN:
                if event.key in [K_a, K_LEFT]:
                    hero_locat = hero_locat.move([-int(lane/2), 0])
                if event.key in [K_d, K_RIGHT]:
                    hero_locat = hero_locat.move([int(lane/2), 0])

        pygame.draw.rect(screen, (96,96,96), (width/2-lane/2, 0, lane, height))
        pygame.draw.rect(screen, (255,255,0), (width/2-line/2, 0, line, height))
        pygame.draw.rect(screen, (252,250,250), (width/2-lane/2 +line*2, 0, line, height))
        pygame.draw.rect(screen, (252,250,250), (width/2+lane/2 -line*2, 0, line, height))

        screen.blit(hero, hero_locat)
        screen.blit(bully, bully_locat)
        pygame.display.update()
        
    pygame.quit()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
