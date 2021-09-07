import pygame
import random
import time
from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_w,
    K_s,
    K_ESCAPE,
    KEYDOWN,
    K_SPACE,
    QUIT,
)

# Define constants for the screen width and height
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Define Font settings
pygame.font.init()
myfont = pygame.font.SysFont('Ariel', 30)

# Left Paddle Class
class Player1(pygame.sprite.Sprite):
    def __init__(self):
        super(Player1, self).__init__()
        self.surf = pygame.Surface((25, 75))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect()
        self.rect = self.surf.get_rect(
            center=(
                20, SCREEN_HEIGHT/2)
        )
    def handle_keys(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_w]:
            self.rect.top = max(20, self.rect.top - 1)
        if key[pygame.K_s]:
            self.rect.bottom = min(SCREEN_HEIGHT - 20, self.rect.bottom + 1)
    def update(self, pressed_keys):
        global ballPosY
        if pressed_keys[K_w]:
            self.rect.move_ip(0, -1)
            if serve == 1:
                ballPosY = self.rect.centery
        if pressed_keys[K_s]:
            self.rect.move_ip(0, 1)
            if serve == 1:
                ballPosY = self.rect.centery
        # Keep player on the screen
        if self.rect.top <= 20:
            self.rect.top = 20
        if self.rect.bottom >= SCREEN_HEIGHT - 20:
            self.rect.bottom = SCREEN_HEIGHT - 20
# Right Paddle class
class Player2(pygame.sprite.Sprite):
    def __init__(self):
        super(Player2, self).__init__()
        self.surf = pygame.Surface((25, 75))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect()
        self.rect = self.surf.get_rect(
            center=(
                SCREEN_WIDTH - 25,SCREEN_HEIGHT/2)
        )
    def handle_keys(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_UP]:
            self.rect.top = max(20, self.rect.top - 1)
        if key[pygame.K_DOWN]:
            self.rect.bottom = min(SCREEN_HEIGHT - 20, self.rect.bottom + 1)
    def update(self, pressed_keys):
        global ballPosY
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -1)
            if serve == 2:
                ballPosY = self.rect.centery
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 1)
            if serve == 2:
                ballPosY = self.rect.centery
        # Keep player on the screen
        if self.rect.top <= 20:
            self.rect.top = 20
        if self.rect.bottom >= SCREEN_HEIGHT -20:
            self.rect.bottom = SCREEN_HEIGHT -20
        
# Initiate sound mixer for future sound
pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=4096)

pygame.init()
window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock=pygame.time.Clock()

player1 = Player1()
player2 = Player2()
ballPosX, ballPosY, ballRadius = player1.rect.right + 11, player1.rect.centery, 10
# Initiate WINNER variable
WINNER = None

v, vel = pygame.math.Vector2(0, 0), 2

serve = 1

#track score
Player1_score = 0
Player2_score = 0

#Populate scoreboard
score = "Player1: " + str(Player1_score) + "    Player2: " + str(Player2_score)
textsurface = myfont.render(score, False, (255, 255, 255))

# Create and populate sprite group
all_sprites = pygame.sprite.Group()
all_sprites.add(player1)
all_sprites.add(player2)

# Sounds
pygame.mixer.set_num_channels(3)
pygame.mixer.music.load('sounds\music.wav')
pygame.mixer.music.play(-1)

wall_snd = pygame.mixer.Sound('sounds\wall.wav')
paddle_snd = pygame.mixer.Sound('sounds\paddle.wav')
score_snd = pygame.mixer.Sound('sounds\score.wav')
win_snd = pygame.mixer.Sound('sounds\win.wav')

# Main Loop
run = True
while run:
    # for loop through the event queue
    for event in pygame.event.get():
        # Check for KEYDOWN event
        if event.type == KEYDOWN:
            # If the Esc key is pressed, then exit the main loop
            if event.key == K_ESCAPE:
                run = False
            if event.key == K_SPACE and v[0] == 0 and v[1] == 0:
                serve = 0
                v[0] = random.choice([-1,1])
                v[1] = random.choice([-1,1])
        # Check for QUIT event. If QUIT, then set running to false.
        elif event.type == QUIT:
            run = False

    # Get all the keys currently pressed
    pressed_keys = pygame.key.get_pressed()

    # Update the player sprite based on user keypresses
    player1.update(pressed_keys)
    player2.update(pressed_keys)

    # ball properties
    min_x, min_y, max_x, max_y = 20, 20, SCREEN_WIDTH - 20, SCREEN_HEIGHT -20

    # Ball X/Y velocity
    ballPosX += v[0] * vel
    ballPosY += v[1] * vel
    
    # Bounce the ball off the top and bottom edges of the screen
    if ballPosY - ballRadius < min_y:
        ballPosY = ballRadius + min_y
        v[1] = -v[1]
        pygame.mixer.Sound.play(wall_snd)
    if ballPosY + ballRadius > max_y:
        ballPosY = max_y - ballRadius
        v[1] = -v[1]
        pygame.mixer.Sound.play(wall_snd)
        
    window.fill((0, 0, 0))

    #Draw scorboard
    window.blit(textsurface,(SCREEN_WIDTH/2 - textsurface.get_rect().width/2,0))
    
    # Draw all sprites
    for entity in all_sprites:
        window.blit(entity.surf, entity.rect)
    # Draw ball
    pygame.draw.circle(window, (255, 255, 255), (round(ballPosX), round(ballPosY)), ballRadius)
    ball = pygame.Rect((0,0), (ballRadius*2, ballRadius*2))
    ball.center = int(ballPosX),int(ballPosY)

    # Handle Left Paddle collision
    if player1.rect.colliderect(ball):
        top = 0
        bottom = 0
        left = 0
        right = 0
        
        if v[0] > 0 :
            top += 1
            bottom +=1
            left += 1
        else :
            top += 1
            bottom += 1
            right += 1
        if v[1] > 0 :
            left += 1
            right += 1
            top += 1
        else :
            left += 1
            right += 1
            bottom += 1

        if ballPosX > player1.rect.x :
            top += 1
            bottom += 1
            right += 1
        else :
            top +=1
            bottom +=1
            left += 1

        if ballPosY > player1.rect.y :
            left += 1
            right += 1
            bottom += 1
        else :
            left += 1
            right += 1
            top += 1

        var = {top:"top", bottom:"bottom",right:"right",left:"left"}
        result = var.get(max(var))
        
        if result == "top" :
            v.reflect_ip(pygame.math.Vector2(0, 1))
            ballPosY = player2.rect.top  - ballRadius
        elif result == "bottom" :
            v.reflect_ip(pygame.math.Vector2(0, 1))
        elif result == "left" :
            v.reflect_ip(pygame.math.Vector2(1, 0))
        elif result == "right" :
            v.reflect_ip(pygame.math.Vector2(1, 0)) 
        pygame.mixer.Sound.play(paddle_snd)
    # Handle Right Paddle collision - same code as above, figure out how to make this one code block           
    if player2.rect.colliderect(ball):
        top = 0
        bottom = 0
        left = 0
        right = 0
        
        if v[0] > 0 :
            top += 1
            bottom +=1
            left += 1
        else :
            top += 1
            bottom += 1
            right += 1
        if v[1] > 0 :
            left += 1
            right += 1
            top += 1
        else :
            left += 1
            right += 1
            bottom += 1

        if ballPosX > player2.rect.x :
            top += 1
            bottom += 1
            right += 1
        else :
            top +=1
            bottom +=1
            left += 1

        if ballPosY > player2.rect.y :
            left += 1
            right += 1
            bottom += 1
        else :
            left += 1
            right += 1
            top += 1

        var = {top:"top", bottom:"bottom",right:"right",left:"left"}
        result = var.get(max(var))
        
        if result == "top" :
            v.reflect_ip(pygame.math.Vector2(0, 1))
            ballPosY = player2.rect.top  - ballRadius
        elif result == "bottom" :
            v.reflect_ip(pygame.math.Vector2(0, 1))
        elif result == "left" :
            v.reflect_ip(pygame.math.Vector2(1, 0))
        elif result == "right" :
            v.reflect_ip(pygame.math.Vector2(1, 0))
        pygame.mixer.Sound.play(paddle_snd)
        
    # Handle ball leaving the screen
    # If ball leaves off Right side, score player 1 and reset ball
    if ballPosX > SCREEN_WIDTH:
        Player1_score = Player1_score + 1
        score = "Player1: " + str(Player1_score) + "    Player2: " + str(Player2_score)
        textsurface = myfont.render(score, False, (255, 255, 255))
        window.blit(textsurface,(SCREEN_WIDTH/2 - textsurface.get_rect().width/2,0))
        pygame.mixer.Sound.play(score_snd)
        ballPosX = player2.rect.left - ballRadius - 1
        ballPosY = player2.rect.centery
        v[0] = 0
        v[1] = 0
        serve = 2
    # If ball leaves off left side, score player 2 and reset ball
    if ballPosX < 0:
        Player2_score = Player2_score + 1
        score = "Player1: " + str(Player1_score) + "    Player2: " + str(Player2_score)
        textsurface = myfont.render(score, False, (255, 255, 255))
        window.blit(textsurface,(SCREEN_WIDTH/2 - textsurface.get_rect().width/2,0))
        pygame.mixer.Sound.play(score_snd)
        ballPosX = player1.rect.right + ballRadius + 1
        ballPosY = player1.rect.centery
        v[0] = 0
        v[1] = 0
        serve = 1
    # Handle Winning
    if Player1_score == 5:    
        WINNER = "PLAYER1"
        break
    if Player2_score == 5:
        WINNER = "PLAYER2"
        break
        
    # Update the display
    pygame.display.flip()

    clock.tick(120)

if WINNER:
    # Draw end screen and wait for ESC or program closing.
    pygame.mixer.music.stop()
    time.sleep(1)
    pygame.mixer.Sound.play(win_snd)
    empty = pygame.Color(0,0,0,0) #The last 0 indicates 0 alpha, a transparent color
    window.fill(empty)
    text1 = WINNER + " has won the game!" 
    textsurface = myfont.render(text1, False, (255, 255, 255))
    text2 = "The Score was " + str(Player1_score) + " to " + str(Player2_score) + "."
    textsurface2 =  myfont.render(text2, False, (255,255,255))
    text3 = "Please press ESC to exit."
    textsurface3 =  myfont.render(text3, False,(255,255,255))
    
    window.blit(textsurface,(SCREEN_WIDTH/2 - textsurface.get_rect().width/2, SCREEN_HEIGHT / 2 - 54))
    window.blit(textsurface2,(SCREEN_WIDTH/2 - textsurface.get_rect().width/2, SCREEN_HEIGHT / 2 + 27 -54))
    window.blit(textsurface3,(SCREEN_WIDTH/2 - textsurface.get_rect().width/2, SCREEN_HEIGHT / 2))
    pygame.display.flip()
    run = True
    
    while run:
        for event in pygame.event.get():
        # Check for KEYDOWN event
            if event.type == KEYDOWN:
                # If the Esc key is pressed, then exit the main loop
                if event.key == K_ESCAPE:
                    run = False
            # Check for QUIT event. If QUIT, then set running to false.
            elif event.type == QUIT:
                run = False    
    
pygame.quit()
