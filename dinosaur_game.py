import pygame
import random
import os
from shop_dino import shop_gui

pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 1200, 400

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (114, 114, 114)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Dinosaur Game')
path = os.path.dirname(os.path.abspath(__file__))

pygame.mixer.music.set_volume(0.05)
pygame.mixer.music.load(path + './res/sounds/Illegals in my Yard (animation).mp3')
pygame.mixer.music.play(-1)

dino_img = pygame.image.load(path + './res/images/dino.png')
cactus_img = pygame.image.load(path + './res/images/cactus.png')
point_img = pygame.image.load(path + './res/images/point.png')

scaled_dino_width, scaled_dino_height = 46, 64  #Left is width & right is height
scaled_cactus_width, scaled_cactus_height = 32, 96
scaled_point_width, scaled_point_height = 64, 32

dino_img = pygame.transform.scale(dino_img, (scaled_dino_width, scaled_dino_height))
cactus_img = pygame.transform.scale(cactus_img, (scaled_cactus_width, scaled_cactus_height))
point_img = pygame.transform.scale(point_img, (scaled_point_width, scaled_point_height))

dino_x, dino_y = 50, HEIGHT - dino_img.get_height()
dino_vel_y = 0
jump = False

cactus_x = WIDTH
cactus_y = HEIGHT - cactus_img.get_height()

point_x = random.randint(WIDTH, WIDTH * 2)
point_y = HEIGHT - point_img.get_height()

score = 0
high_score = 0
font = pygame.font.Font(None, 36)

def draw_dino_nametag():
    text_pos = dino_y - 30
    text = font.render('Nigger', True, BLACK)
    screen.blit(text, (dino_x, text_pos))

def draw_dino():
    screen.blit(dino_img, (dino_x, dino_y))

def draw_cactus():
    screen.blit(cactus_img, (cactus_x, cactus_y))

def draw_point():
    screen.blit(point_img, (point_x, point_y))

def draw_score():
    text = font.render(f'Score: {score}', True, BLACK)
    screen.blit(text, (10, 10))

def set_high_score(final_score):
    global high_score
    if final_score >= high_score:
        high_score = final_score

def draw_game_over(final_score):
    font_big = pygame.font.Font(None, 72)
    text_game_over = font_big.render('You Died', True, BLACK)
    text_final_score = font.render(f'Final Score: {final_score}', True, BLACK)
    text_respawn = font.render('Press Space to Restart', True, BLACK)

    screen.blit(text_game_over, (WIDTH // 2 - text_game_over.get_width() // 2, HEIGHT // 3 - text_game_over.get_height() // 2))
    screen.blit(text_final_score, (WIDTH // 2 - text_final_score.get_width() // 2, HEIGHT // 2 - text_final_score.get_height() // 2))
    screen.blit(text_respawn, (WIDTH // 2 - text_respawn.get_width() // 2, HEIGHT * 2 // 3 - text_respawn.get_height() // 2))
    draw_shop_button()

def draw_high_score():
    text = font.render(f'High Score: {high_score}', True, BLACK)
    screen.blit(text, (525, 10))

def generate_point_position(cactus_x, cactus_width, min_distance=100):
    point_x = random.randint(WIDTH, WIDTH * 2)
    while abs(point_x - (cactus_x + cactus_width)) < min_distance:
        point_x = random.randint(WIDTH, WIDTH * 2)
    return point_x

def reset_game():
    global cactus_x, score, point_x
    cactus_x = WIDTH
    score = 0
    point_x = generate_point_position(cactus_x, scaled_cactus_width)

def draw_shop_button():
    font_button = pygame.font.Font(None, 36)
    text_button = font_button.render('Press S to Open Shop', True, BLACK)
    screen.blit(text_button, (WIDTH // 2 - text_button.get_width() // 2, HEIGHT - 60))

def main():
    global dino_y, dino_vel_y, jump, cactus_x, score, point_x

    clock = pygame.time.Clock()
    game_over = False
    random_speed = 6
    back_to_death_screen = False 

    background = pygame.Surface(screen.get_size())
    background.fill(WHITE)

    while True:
        clock.tick(120)
        screen.fill(WHITE)

        draw_dino()
        draw_dino_nametag()
        draw_cactus()
        draw_point()
        draw_score()
        draw_high_score()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not jump:
                    jump = True
                    dino_vel_y = -20

                if game_over == True:
                    if event.key == pygame.K_SPACE:
                        reset_game()
                        game_over = False
                        dino_y = HEIGHT - dino_img.get_height()
                        jump = False
                        cactus_x = WIDTH

                    if event.key == pygame.K_s:
                        back_to_death_screen = shop_gui()
                        
        if not game_over:
            if jump:
                dino_y += dino_vel_y
                dino_vel_y += 1
                if dino_y >= HEIGHT - dino_img.get_height():
                    dino_y = HEIGHT - dino_img.get_height()
                    jump = False

            if cactus_x < -cactus_img.get_width():
                cactus_x = WIDTH
                score += 1
                random_speed = random.randint(5, 12)

            if point_x < -point_img.get_width():
                point_x = generate_point_position(cactus_x, scaled_cactus_width)
                    
            cactus_x -= random_speed
            point_x -= random_speed

        else:
            draw_game_over(score)

        pygame.display.update()

        dino_rect = pygame.Rect(dino_x, dino_y, dino_img.get_width(), dino_img.get_height())
        cactus_rect = pygame.Rect(cactus_x, cactus_y, cactus_img.get_width(), cactus_img.get_height())
        point_rect = pygame.Rect(point_x, point_y, point_img.get_width(), point_img.get_height())

        if dino_rect.colliderect(cactus_rect):
            set_high_score(score)
            game_over = True
        elif dino_rect.colliderect(point_rect):
            score += 1 
            point_x = random.randint(WIDTH, WIDTH * 2)

if __name__ == '__main__':
    main()