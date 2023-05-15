import pygame
import pygame_gui
import os
from shop_dino import shop_gui

pygame.init()
path = os.path.dirname(os.path.abspath(__file__))

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

pygame.display.set_caption('Dino Game')
window_surface = pygame.display.set_mode((1200, 400))

background = pygame.Surface((1200, 400))
background.fill(pygame.Color('#FFFFFF'))

manager = pygame_gui.UIManager((1200, 400))
font = pygame.font.Font(None, 36)

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

file_path = path + "/res/Perm_point.txt"
total_points = load_points(file_path)

def draw_title():
    text = font.render('Dino Game', True, BLACK)
    window_surface.blit(text, (525, 100))

pygame.mixer.music.set_volume(0.05)
pygame.mixer.music.load(path + '/res/sounds/Illegals in my Yard (animation).mp3')
pygame.mixer.music.play(-1)


play_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((540, 170), (100, 50)),
                                            text='Play',
                                            manager=manager)

shop_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((540, 230), (100, 50)),
                                           text="Shop",
                                           manager=manager)

mute_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((20, 10), (100, 50)),
                                           text="Mute",
                                           manager=manager)

clock = pygame.time.Clock()
is_running = True
start_game = False
mute = False

def main_menu():
    global start_game, is_running, mute
    while is_running:
        time_delta = clock.tick(60)/1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
            
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == play_button:
                    start_game = True
                    is_running = False
                    
                if event.ui_element == shop_button:
                    shop_gui(window_surface, True, total_points)
                                
                if event.ui_element == mute_button:
                    if not mute:
                        pygame.mixer.music.set_volume(0)
                        mute = True
   
                    else:
                        pygame.mixer.music.set_volume(0.05)
                        mute = False       

            manager.process_events(event)
        
        manager.update(time_delta)

        window_surface.blit(background, (0, 0))
        manager.draw_ui(window_surface)
        draw_title()

        pygame.display.update()
    
    return start_game
    

if __name__ == "__main__":
    main_menu()
    