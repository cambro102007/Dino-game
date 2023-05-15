import pygame
import random
import os
import math
from shop_dino import shop_gui
from main_menu import main_menu
from shop_dino import purchased_boxes


pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 1200, 400

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (114, 114, 114)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
path = os.path.dirname(os.path.abspath(__file__))

dino_animation_cooldown = 100
current_dino_frame = 0
last_update = pygame.time.get_ticks()

dino_frames = ['/res/images/man_running_1.png',
               '/res/images/man_running_2.png',
               '/res/images/man_running_3.png',
               '/res/images/man_running_4.png']
dino_dead = pygame.image.load(path + '/res/images/man_dead_1.png')
cactus_img = pygame.image.load(path + '/res/images/cactus.png')
point_img = pygame.image.load(path + '/res/images/point.png')
dino_img = pygame.image.load(path + '/res/images/man_running_1.png')
background_img = pygame.image.load(path + '/res/images/background.png')
file_path = path + "/res/Perm_point.txt"

background_width = background_img.get_width()

scaled_dino_width, scaled_dino_height = 84, 120  #Left is width & right is height
scaled_cactus_width, scaled_cactus_height = 32, 96
scaled_point_width, scaled_point_height = 64, 32

cactus_img = pygame.transform.scale(cactus_img, (scaled_cactus_width, scaled_cactus_height))
point_img = pygame.transform.scale(point_img, (scaled_point_width, scaled_point_height))
dino_dead = pygame.transform.scale(dino_dead, (scaled_dino_width + 40, scaled_dino_height + 4))

dino_x, dino_y = 50, HEIGHT - scaled_dino_height
dino_vel_y = 0
jump = False

cactus_x = WIDTH
cactus_y = HEIGHT - cactus_img.get_height()

played_before = os.stat(path + "/res/highscore.txt")

if played_before.st_size == 0:
    f = open(path + "/res/highscore.txt", "w")
    f.write("0")
    f.close()

point_x = random.randint(WIDTH, WIDTH * 2)
point_y = HEIGHT - point_img.get_height()

high_score_file = open(path + "/res/highscore.txt")
high_score = high_score_file.read()
high_score_file.close()

score = 0
font = pygame.font.Font(None, 36)

def draw_dino_nametag():
    text_pos = dino_y - 30
    text = font.render('', True, WHITE)
    screen.blit(text, (dino_x, text_pos))

def draw_dino(frame):
    global transformed_img
    dino_image_frame = pygame.image.load(path + dino_frames[frame])
    transformed_img = pygame.transform.scale(dino_image_frame, (scaled_dino_width, scaled_dino_height))
    screen.blit(transformed_img, (dino_x, dino_y))
    draw_dino_nametag()

def draw_cactus():
    screen.blit(cactus_img, (cactus_x, cactus_y))

def draw_point():
    screen.blit(point_img, (point_x, point_y))

def draw_score():
    text = font.render(f'Score: {score}', True, WHITE)
    screen.blit(text, (10, 10))

def set_high_score(final_score):
    global high_score
    global high_score_int 
    high_score_int = int(high_score)
    if final_score >= high_score_int:
        high_score = final_score
    save_highscore(high_score.__str__())

def draw_game_over(final_score):
    font_big = pygame.font.Font(None, 72)
    text_game_over = font_big.render('You Died', True, WHITE)
    text_final_score = font.render(f'Final Score: {final_score}', True, WHITE)
    text_respawn = font.render('Press Space to Restart', True, WHITE)

    screen.blit(text_game_over, (WIDTH // 2 - text_game_over.get_width() // 2, HEIGHT // 3 - text_game_over.get_height() // 2))
    screen.blit(text_final_score, (WIDTH // 2 - text_final_score.get_width() // 2, HEIGHT // 2 - text_final_score.get_height() // 2))
    screen.blit(text_respawn, (WIDTH // 2 - text_respawn.get_width() // 2, HEIGHT * 2 // 3 - text_respawn.get_height() // 2))
    draw_shop_button()
    draw_menu_button()
    
def draw_high_score():
    text = font.render(f'High Score: {high_score}', True, WHITE)
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
    text_button = font_button.render('Press S to Open Shop', True, WHITE)
    screen.blit(text_button, (WIDTH // 2 - text_button.get_width() // 2, HEIGHT - 70))
    
def draw_menu_button():
    font_button = pygame.font.Font(None, 36)
    text_button = font_button.render('Press M to go back to the Menu', True, WHITE)
    screen.blit(text_button, (WIDTH // 2 - text_button.get_width() // 2, HEIGHT - 109)) 
    
def save_highscore(highscore):
    f = open(path + "/res/highscore.txt", "w")
    f.write(highscore)
    f.close()

def draw_dead_dino():
    screen.blit(dino_dead, (dino_x, dino_y))
    text_pos = dino_y - 30
    text = font.render('Dead ', True, BLACK)
    screen.blit(text, (dino_x, text_pos))
    
def animate_dino(ct, lu, cd):
    global current_dino_frame, last_update
    if ct - lu >= cd:
        current_dino_frame += 1
        last_update = ct
    if current_dino_frame >= len(dino_frames):
            current_dino_frame = 0        

def load_points(file_path):
    if file_exists(file_path):
        content = read_file(file_path)
        points = int(content)
    else:
        points = 0

    return points

def file_exists(file_path):
    return os.path.exists(file_path)

def read_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    return content

def save_points(file_path, points):
    with open(file_path, 'w') as file:
        file.write(str(points))

def load_points(file_path):
    if not file_exists(file_path):
        return 0
    else:
        with open(file_path, 'r') as file:
            content = file.read()
            if content.strip() == '':
                return 0
            elif content.isdigit():
                return int(content)
            else:
                print(f"Invalid content in file '{file_path}': '{content}'")
                return 0

def write_file(file_path, content):
    with open(file_path, 'w') as file:
        file.write(content)

def main():
    global dino_y, dino_x, dino_vel_y, jump, cactus_x, score, point_x, current_dino_frame, last_update
    global total_points
    
    clock = pygame.time.Clock()
    game_over = False
    random_speed = 6
    back_to_death_screen = False 
    scroll = 0
    tiles = math.ceil(WIDTH / background_width) + 1
    
    try:
        while main_menu() == True:
            pygame.display.set_caption('Dinosaur Game')
            clock.tick(120)
            current_time = pygame.time.get_ticks()
            
            if game_over == False:
                for i in range(0, tiles):
                    screen.blit(background_img, (i * background_width + scroll, -320))
                scroll -= 5
            else:
                for i in range(0, tiles):
                    screen.blit(background_img, (i * background_width + scroll, -320))
                scroll -= 0
            
            draw_cactus()
            draw_point()
            draw_score()
            draw_high_score()
            total_points = load_points(file_path)
            

            if abs(scroll) > background_width:
                scroll = 0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                    
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and not jump or event.key == pygame.K_UP and not jump:
                        jump = True
                        
                        if purchased_boxes["Box 1"]:
                            dino_vel_y = -23
                        else:
                            dino_vel_y = -20
              
                    if game_over == True:
                        if event.key == pygame.K_SPACE:
                            reset_game()
                            game_over = False
                            dino_y = HEIGHT - scaled_dino_height
                            jump = False
                            cactus_x = WIDTH

                        if event.key == pygame.K_s:
                            shop_gui(screen, True, total_points)

                        if event.key == pygame.K_m:
                            main_menu()
                            return

            if not game_over:
                draw_dino(current_dino_frame)
                if jump:
                    dino_y += dino_vel_y
                    dino_vel_y += 1
                    if dino_y >= HEIGHT - transformed_img.get_height():
                        dino_y = HEIGHT - transformed_img.get_height()
                        jump = False

                if cactus_x < -cactus_img.get_width():
                    cactus_x = WIDTH
                    score += 1
                    random_speed = random.randint(5, 12)

                if point_x < -point_img.get_width():
                    point_x = generate_point_position(cactus_x, scaled_cactus_width)
                        
                cactus_x -= random_speed
                point_x -= random_speed
                
                if random_speed < 6:
                    cooldown = 200
                elif random_speed < 8:
                    cooldown = 175
                elif random_speed < 10:
                    cooldown = 125
                elif random_speed < 13:
                    cooldown = 75
                
                animate_dino(current_time, last_update, cooldown)
                
            else:
                draw_game_over(score)
                draw_dead_dino()

            pygame.display.update()

            dino_rect = pygame.Rect(dino_x, dino_y, transformed_img.get_width(), transformed_img.get_height())
            cactus_rect = pygame.Rect(cactus_x, cactus_y, cactus_img.get_width(), cactus_img.get_height())
            point_rect = pygame.Rect(point_x, point_y, point_img.get_width(), point_img.get_height())

            if dino_rect.colliderect(cactus_rect):
                set_high_score(score)
                game_over = True
            if dino_rect.colliderect(point_rect):
                score += 1 
                total_points += 1
                save_points(file_path, total_points)
                point_x = random.randint(WIDTH, WIDTH * 2)

    finally:
        save_points(file_path, total_points)
        pygame.quit()

if __name__ == '__main__':
    main()