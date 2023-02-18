import pygame
import os
pygame.font.init()
pygame.mixer.init()

pygame.init
pygame.display.set_caption("GUNFIGHT")

FPS = 60
VELOCITY = 4.5
BULLET_VELOCITY = 12
MAX_BULLETS = 3
BLACK = (0,0,0)
WHITE = (255,255,255)
YELLOW = (255,255,51)
WIDTH, HEIGHT = 1280,720
CHAR_WIDTH , CHAR_HEIGHT = 128,105
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)

GUNSHOT = pygame.mixer.Sound('Assets/gunshot.mp3')
HIT_SOUND = pygame.mixer.Sound('Assets/oof.mp3')
NARUTO_WINS = pygame.mixer.Sound('Assets/NARUTO_WINS.mp3')
SASUKE_WINS = pygame.mixer.Sound('Assets/SASUKE_WINS.mp3')
BYE = pygame.mixer.Sound('Assets/BYE.mp3')

NARUTO_HIT = pygame.USEREVENT + 1
SASUKE_HIT = pygame.USEREVENT + 2
HEALTH_FONT = pygame.font.Font(os.path.join('Assets','font.ttf'),50)
GG_FONT = pygame.font.Font(os.path.join('Assets','font.ttf'),120)

NARUTO_IMG = pygame.image.load(os.path.join('Assets', 'naruto.png'))
SASUKE_IMG = pygame.image.load(os.path.join('Assets', 'sasuke.png'))
NARUTO_HIT_IMG = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'naruto_hit.png')),(CHAR_WIDTH,CHAR_HEIGHT))
SASUKE_HIT_IMG = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'sasuke_hit.png')),(CHAR_WIDTH,CHAR_HEIGHT))

BG = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'background.png')),(WIDTH,HEIGHT))
NARUTO= pygame.transform.scale(NARUTO_IMG,(CHAR_WIDTH,CHAR_HEIGHT))
SASUKE= pygame.transform.scale(SASUKE_IMG,(CHAR_WIDTH,CHAR_HEIGHT))

def manage_bullets(naruto_bullets, sasuke_bullets, orange, blue):
    for bullet in naruto_bullets:
        bullet.x += BULLET_VELOCITY
        if blue.colliderect(bullet):
            pygame.event.post(pygame.event.Event(SASUKE_HIT))
            naruto_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            naruto_bullets.remove(bullet)

    for bullet in sasuke_bullets:
        bullet.x -= BULLET_VELOCITY
        if orange.colliderect(bullet):
            pygame.event.post(pygame.event.Event(NARUTO_HIT))
            sasuke_bullets.remove(bullet)
        elif bullet.x < 0:
            sasuke_bullets.remove(bullet)

def draw_window(orange,blue, naruto_bullets, sasuke_bullets , NARUTO_HEALTH , SASUKE_HEALTH,event):
    WIN.blit(BG , (0,0))
    #pygame.draw.rect(WIN,YELLOW,BORDER)
    naruto_health_text = HEALTH_FONT.render("HP: " + str(NARUTO_HEALTH), 1, (255,165,0))
    sasuke_health_text = HEALTH_FONT.render("HP: " + str(SASUKE_HEALTH), 1, (173,216,230) )
    WIN.blit(sasuke_health_text, (WIDTH - sasuke_health_text.get_width() - 10, 10))
    WIN.blit(naruto_health_text, (10, 10))
    WIN.blit(NARUTO,(orange.x,orange.y))
    WIN.blit(SASUKE,(blue.x,blue.y))
    if event.type == NARUTO_HIT:
        WIN.blit(NARUTO_HIT_IMG,(orange.x,orange.y))
    if event.type == SASUKE_HIT:
        WIN.blit(SASUKE_HIT_IMG,(blue.x,blue.y))

    for bullet in naruto_bullets:
        pygame.draw.rect(WIN, (255,0,0), bullet)

    for bullet in sasuke_bullets:
        pygame.draw.rect(WIN,(12,47,223), bullet)

    pygame.display.update()    

def naruto_moves(keys_pressed,orange):
    if keys_pressed[pygame.K_a] and orange.x - VELOCITY > 50:  
        orange.x -= VELOCITY
    if keys_pressed[pygame.K_d] and orange.x + orange.width + VELOCITY  < BORDER.x:  
        orange.x += VELOCITY    
    if keys_pressed[pygame.K_w] and orange.y - VELOCITY > 150:  
        orange.y -= VELOCITY
    if keys_pressed[pygame.K_s] and orange.y + VELOCITY + orange.height < HEIGHT:  
        orange.y += VELOCITY

def sasuke_moves(keys_pressed,blue):
    if keys_pressed[pygame.K_LEFT] and blue.x - VELOCITY > BORDER.x :  
        blue.x -= VELOCITY
    if keys_pressed[pygame.K_RIGHT] and blue.x + blue.width + VELOCITY  < WIDTH - 50:  
        blue.x += VELOCITY    
    if keys_pressed[pygame.K_UP] and blue.y - VELOCITY > 150:  
        blue.y -= VELOCITY
    if keys_pressed[pygame.K_DOWN] and blue.y + VELOCITY + blue.height < HEIGHT:  
        blue.y += VELOCITY

def draw_winner(text,gg_color,gg_sound):
    draw_text = GG_FONT.render(text, 1, gg_color)
    gg_sound.play()
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width() /
                         2, HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(4000)

def main():
    orange = pygame.Rect(50, 280, CHAR_WIDTH, CHAR_HEIGHT)
    blue = pygame.Rect(1030, 280, CHAR_WIDTH, CHAR_HEIGHT)

    naruto_bullets = []
    sasuke_bullets = []

    NARUTO_HEALTH = 100
    SASUKE_HEALTH = 100  

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            #quit game
            if event.type == pygame.QUIT:
                BYE.play()
                pygame.time.delay(1550)
                run = False  
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LSHIFT and len(naruto_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(orange.x + orange.width, orange.y + orange.height//2 - 13 , 13, 5)
                    naruto_bullets.append(bullet)
                    GUNSHOT.play()

                if event.key == pygame.K_SPACE and len(sasuke_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(blue.x, blue.y + blue.height//2 -2 , 13, 5)
                    sasuke_bullets.append(bullet)
                    GUNSHOT.play()

            if event.type == NARUTO_HIT:
                NARUTO_HEALTH -= 10
                HIT_SOUND.play()
   
            if event.type == SASUKE_HIT:
                SASUKE_HEALTH -= 10
                HIT_SOUND.play()
        gg = ""
        if NARUTO_HEALTH <= 0:
            gg = "Sasuke Wins!"
            gg_color = (173,216,230)
            gg_sound = SASUKE_WINS

        if SASUKE_HEALTH <= 0:
            gg = "Naruto Wins!"    
            gg_color = (255,165,0)
            gg_sound = NARUTO_WINS

        if gg != "":
            draw_winner(gg,gg_color,gg_sound) 
            break

        keys_pressed = pygame.key.get_pressed()
        naruto_moves(keys_pressed,orange)
        sasuke_moves(keys_pressed,blue)
        manage_bullets(naruto_bullets, sasuke_bullets, orange, blue)
        draw_window(orange, blue, naruto_bullets, sasuke_bullets, NARUTO_HEALTH , SASUKE_HEALTH,event)

    main()

if __name__ == "__main__":
    main()
