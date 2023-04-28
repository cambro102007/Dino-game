import pygame
import os

pygame.init()

WIDTH, HEIGHT = 1200, 400

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (180, 180, 180)

def buy_box():
    global total_points, box1_bought, dino_jump_vel
    if not box1_bought and total_points >= 500:
        total_points -= 500
        box1_bought = True
        dino_jump_vel = -25
        save_box1_bought()

def save_box1_bought():
    with open(box1_path, 'w') as file:
        file.write(str(box1_bought))

def file_exists(file_path):
    return os.path.exists(file_path)

def load_box1_bought():
    global box1_bought
    path = os.path.dirname(os.path.abspath(__file__))
    box1_path = os.path.join(path, 'res', 'box1.txt')
    if os.path.exists(box1_path):
        with open(box1_path, 'r') as f:
            box1_bought = f.read().strip() == 'True'
    else:
        box1_bought = False

def shop_gui(screen, total_points, box1_path):
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Dino Shop')

    font = pygame.font.Font(None, 36)
    exit_text = font.render('Click S to exit', True, BLACK)

    box_width, box_height = (WIDTH - 10) // 6, HEIGHT - 50
    box_texts = ['Box 1', 'Box 2', 'Box 3', 'Box 4', 'Box 5', 'Box 6']
    boxes = []
    box_rects = []
    
    for i, text in enumerate(box_texts):
        box = pygame.Surface((box_width, box_height))
        box.fill(GREY)
        box_text = font.render(text, True, BLACK)
        box.blit(box_text, (box_width // 2 - box_text.get_width() // 2, box_height - box_text.get_height()))
        box_rect = box.get_rect()
        box_rect.x = i * (box_width + 2)
        box_rect.y = HEIGHT - box_height
        boxes.append(box)
        box_rects.append(box_rect)

    box1_text = font.render('Box 1', True, BLACK)
    box1_price_text = font.render('500 points', True, BLACK)
    box1_bought_text = font.render('Bought', True, BLACK)
    box1_rect = pygame.Rect(0, 0, box_width, box_height)
    box1_rect.x = 0
    box1_rect.y = HEIGHT - box_height
    box1_bought = load_box1_bought()

    def draw_total_points_shop():
        text = font.render(f'Total Points: {total_points}', True, BLACK)
        screen.blit(text, (WIDTH - text.get_width() - 10, 10))

    running = True
    back_to_death_screen = False
    while running:
        screen.fill(WHITE)

        screen.blit(exit_text, (WIDTH // 2 - exit_text.get_width() // 2, 10))

        if box1_bought:
            screen.blit(box1_bought_text, (box1_rect.x + box_width // 2 - box1_bought_text.get_width() // 2, box1_rect.y + box_height // 2 - box1_bought_text.get_height() // 2))
        else:
            screen.blit(box1_text, (box1_rect.x + box_width // 2 - box1_text.get_width() // 2, box1_rect.y + box_height // 2 - box1_text.get_height() // 2))
            screen.blit(box1_price_text, (box1_rect.x + box_width // 2 - box1_price_text.get_width() // 2, box1_rect.y + box_height - box1_price_text.get_height()))
        
        for box in boxes:
            screen.blit(box, (boxes.index(box) * (box_width + 2), HEIGHT - box_height))

        for i in range(1, 6):
            pygame.draw.line(screen, BLACK, (i * (box_width + 2) - 1, HEIGHT - box_height), (i * (box_width + 2) - 1, HEIGHT), 2)

        draw_total_points_shop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                if box1_rect.collidepoint(mouse_pos):
                    buy_box()

        pygame.display.update()

    return back_to_death_screen

if __name__ == "__main__":
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    total_points = 0
    box1_path = 'res/box1.txt'
    shop_gui(screen, total_points, box1_path)