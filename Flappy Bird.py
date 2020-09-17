import pygame
import sys
import random


def draw_base():
    window.blit(base_image, (base_x, 450))
    window.blit(base_image, (base_x + 288, 450))

def create_pipe():
    random_height = random.choice(pipe_height)
    bottom_pipe =pipe_surface.get_rect(midtop=(350, random_height))
    top_pipe =pipe_surface.get_rect(midbottom=(350, random_height-150))
    return bottom_pipe, top_pipe

def move_pipe(pipes):
    for pipe in pipes:
        pipe.centerx = int(pipe.centerx - 2.5)
    return pipes

def draw_pipe(pipes):
    for pipe in pipes:
        if pipe.bottom >= 512:
            window.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            window.blit(flip_pipe, pipe)

def check_collission(pipes):
    for pipe in pipes:
        if bird_rectangle.colliderect(pipe):
            collision_sound.play()
            return False
        if bird_rectangle.top <= -50 or bird_rectangle.bottom >= 450:
            collision_sound.play()
            return False
    return True

def rotate_bird():
    new_bird = pygame.transform.rotozoom(bird_surface, -bird_movement * 3, 1)
    return new_bird

def bird_animation():
    new_bird = bird_frames[bird_index]
    new_bird_rect = new_bird.get_rect(center = (50, bird_rectangle.centery))
    return new_bird,new_bird_rect


def score_display(game_state):
    if game_state == 'current_game':
        score_surface = game_font.render(str(int(score)),True,(255,255,255))
        score_rect = score_surface.get_rect(center = (144,50))
        window.blit(score_surface,score_rect)
    if game_state == 'game_over':
        score_surface = game_font.render(f'Score:{int(score)}',True,(255,255,255))
        score_rect = score_surface.get_rect(center = (144,50))
        window.blit(score_surface,score_rect)

        high_score_surface = game_font.render(f'High Score:{int(high_score)}',True,(255,255,255))
        high_score_rect = high_score_surface.get_rect(center = (144,425))
        window.blit(high_score_surface,high_score_rect)



#initializing
pygame.init()
WIDTH = 288
HEIGHT = 512
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("FLAPPY BIRD @TM")
clock = pygame.time.Clock()


#images
#background
background_image = pygame.image.load(r"assets\background-day.png").convert()
background_pos = (0,0)


#base
base_image = pygame.image.load(r"assets\base.png").convert()
base_x = 0


#bird
bird_downflap = pygame.image.load('assets/bluebird-downflap.png').convert_alpha()
bird_midflap = pygame.image.load('assets/bluebird-midflap.png').convert_alpha()
bird_upflap = pygame.image.load('assets/bluebird-upflap.png').convert_alpha()
bird_frames = [bird_downflap,bird_midflap,bird_upflap]
bird_index = 0
bird_surface = bird_frames[bird_index]
bird_rectangle = bird_surface.get_rect(center = (50,256))

BIRDFLAP = pygame.USEREVENT
pygame.time.set_timer(BIRDFLAP,60)

#pipe
pipe_surface = pygame.image.load(r"assets\pipe-green.png").convert()
pipe_list = []
pipe_height = [200,300,400]
SWAMP = pygame.USEREVENT
pygame.time.set_timer(SWAMP, 1200)

#Game over
game_over_surface = pygame.image.load('assets/gameover.png').convert_alpha()
game_over_rect = game_over_surface.get_rect(center =(144,256))

#Game variable
gravity = 0.15
bird_movement = 0
game = True
game_font = pygame.font.Font('04B_19.ttf',40)

score = 0
high_score = 0


#music
flap_sound = pygame.mixer.Sound('sound/sfx_wing.wav')
collision_sound = pygame.mixer.Sound('sound/sfx_hit.wav')
score_sound = pygame.mixer.Sound('sound/sfx_point.wav')
score_sound_countdown = 100

#game loop
while True:
    clock.tick(120)

    for event in pygame.event.get():
        keys = pygame.key.get_pressed()

        if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
            pygame.quit()
            sys.exit()

        if keys[pygame.K_SPACE] and game:
            bird_movement = 0
            bird_movement -= 3
            flap_sound.play()

        if event.type == SWAMP:
            pipe_list.extend(create_pipe())
            if len(pipe_list) > 3:
                pipe_list = pipe_list[-3:]

        if keys[pygame.K_SPACE] and game == False:
            game = True
            pipe_list.clear()
            bird_rectangle.center = (50, 256)
            bird_movement = 0
            score = 0

        if event.type == BIRDFLAP:
            bird_index = (bird_index+1) % 3

    bird_surface, bird_rectangle = bird_animation()

    window.blit(background_image, background_pos)

    if game:
        #bird
        bird_movement += gravity
        bird_rectangle.centery = int(bird_rectangle.centery+bird_movement)
        window.blit(rotate_bird(), bird_rectangle)
        #pipes
        pipe_list = move_pipe(pipe_list)
        draw_pipe(pipe_list)
        score += 0.01
        score_sound_countdown -= 1
        if score_sound_countdown <= 0:
            score_sound.play()
            score_sound_countdown = 100
        score_display("current_game")
        game = check_collission(pipe_list)
    else :
        window.blit(game_over_surface,game_over_rect)
        high_score = max(score,high_score)
        score_display('game_over')


    #base
    # creates flow animation at the base
    base_x = (base_x - 1) % -288
    draw_base()
    pygame.display.update()