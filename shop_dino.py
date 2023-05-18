import pygame
import yaml
import os

pygame.init()

WIDTH, HEIGHT = 1200, 400

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (180, 180, 180)

path = os.path.dirname(os.path.abspath(__file__))

def save_purchased_boxes(purchased_boxes):
    with open('box_purchase.yaml', 'w') as f:
        yaml.dump(purchased_boxes, f)

def load_purchased_boxes():
    try:
        with open('box_purchase.yaml', 'r') as f:
            purchased_boxes = yaml.safe_load(f)
    except FileNotFoundError:

        purchased_boxes = {"Box 1": False}
        save_purchased_boxes(purchased_boxes)

    return purchased_boxes

purchased_boxes = load_purchased_boxes()

def save_Perm_point(Perm_point):
    f = open(path + "/res/Perm_point.txt", "w")
    f.write(Perm_point)
    f.close()

def shop_gui(screen, is_running):
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Dino Shop')
    
    def remove_points(points_to_remove):
        Perm_point_file = open(path + "/res/Perm_point.txt", "r+")
        points = int(Perm_point_file.read().strip())        
        if purchased_boxes["Box 1"] == True or purchased_boxes["Box 2"] == True:
            points -= points_to_remove
            Perm_point_file.write(str(points))
            Perm_point_file.close()

        save_Perm_point(points.__str__())

    font = pygame.font.Font(None, 36)
    exit_text = font.render('Click S to exit', True, BLACK)

    box_width, box_height = (WIDTH - 10) // 6, HEIGHT - 50
    box_texts = ['500 Points', '250 Points', 'Box 3', 'Box 4', 'Box 5', 'Box 6']
    boxes = []
    box_rects = []
    
    for i, text in enumerate(box_texts):
        box = pygame.Surface((box_width, box_height))
        box.fill(GREY)
        if i == 0 and purchased_boxes["Box 1"]:
            text = font.render('Purchased', True, BLACK)
        elif i == 1 and purchased_boxes["Box 2"]:
            text = font.render('Purchased', True, BLACK)           
        else:
            text = font.render(text, True, BLACK)
        box.blit(text, (box_width // 2 - text.get_width() // 2, box_height - text.get_height()))
        box_rect = box.get_rect()
        box_rect.x = i * (box_width + 2)
        box_rect.y = HEIGHT - box_height - 50
        boxes.append(box)
        box_rects.append(box_rect.copy())

    def draw_total_points_shop(points):
        text = font.render(f'Total Points: {points}', True, BLACK)
        screen.blit(text, (WIDTH - text.get_width() - 10, 10))

    running = is_running
    back_to_death_screen = False
    
    while running:
        perm_point_file = open(path + "/res/Perm_point.txt", "r+")
        total_points = int(perm_point_file.read().strip())
        perm_point_file.close()
        screen.fill(WHITE)

        screen.blit(exit_text, (WIDTH // 2 - exit_text.get_width() // 2, 10))

        for box in boxes:
            screen.blit(box, (boxes.index(box) * (box_width + 2), HEIGHT - box_height))

        for i in range(1, 6):
            pygame.draw.line(screen, BLACK, (i * (box_width + 2) - 1, HEIGHT - box_height), (i * (box_width + 2) - 1, HEIGHT), 2)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    back_to_death_screen = True
                    running = False
            
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for i, box_rect in enumerate(box_rects):
                    if box_rect.collidepoint(event.pos):
                        if i == 0 and not purchased_boxes.get("Box 1") and total_points >= 500:
                            purchased_boxes["Box 1"] = True
                            save_purchased_boxes(purchased_boxes)
                            remove_points(500)
                            box = pygame.Surface((box_width, box_height))
                            box.fill(GREY)
                            text = font.render('Purchased', True, BLACK)
                            box.blit(text, (box_width // 2 - text.get_width() // 2, box_height - text.get_height()))
                            boxes[i] = box
                        
                        elif i == 1 and not purchased_boxes.get("Box 2") and total_points >= 250:
                            purchased_boxes["Box 2"] = True
                            save_purchased_boxes(purchased_boxes)
                            remove_points(250)
                            box = pygame.Surface((box_width, box_height))
                            box.fill(GREY)
                            text = font.render('Purchased', True, BLACK)
                            box.blit(text, (box_width // 2 - text.get_width() // 2, box_height - text.get_height()))
                            boxes[i] = box         
                
                
        draw_total_points_shop(total_points)
        
        pygame.display.update()

    return back_to_death_screen, total_points

if __name__ == "__main__":
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    shop_gui(screen, True)