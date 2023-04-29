import pygame

pygame.init()

WIDTH, HEIGHT = 1200, 400

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (180, 180, 180)

higher_jumps_purchased = False

def shop_gui(screen, total_points):
    global dino_vel_y
    global higher_jumps_purchased
    
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Dino Shop')

    font = pygame.font.Font(None, 36)
    exit_text = font.render('Click S to exit', True, BLACK)

    box_width, box_height = (WIDTH - 10) // 6, HEIGHT - 50
    box_texts = ['500 points to purchase', 'Box 2', 'Box 3', 'Box 4', 'Box 5', 'Box 6']
    boxes = []
    box_rects = []
    global purchased_boxes
    purchased_boxes = [False] * len(box_texts)
    
    
    for i, text in enumerate(box_texts):
        box = pygame.Surface((box_width, box_height))
        box.fill(GREY)
        if i == 0 and purchased_boxes[i]:
            text = font.render('Purchased', True, BLACK)
        else:
            text = font.render(text, True, BLACK)
        box.blit(text, (box_width // 2 - text.get_width() // 2, box_height - text.get_height()))
        box_rect = box.get_rect()
        box_rect.x = i * (box_width + 2)
        box_rect.y = HEIGHT - box_height - 50
        boxes.append(box)
        box_rects.append(box_rect.copy())

    def draw_total_points_shop():
        text = font.render(f'Total Points: {total_points}', True, BLACK)
        screen.blit(text, (WIDTH - text.get_width() - 10, 10))

    running = True
    back_to_death_screen = False
    
    while running:
        screen.fill(WHITE)

        screen.blit(exit_text, (WIDTH // 2 - exit_text.get_width() // 2, 10))

        for box in boxes:
            screen.blit(box, (boxes.index(box) * (box_width + 2), HEIGHT - box_height))

        for i in range(1, 6):
            pygame.draw.line(screen, BLACK, (i * (box_width + 2) - 1, HEIGHT - box_height), (i * (box_width + 2) - 1, HEIGHT), 2)

        draw_total_points_shop()

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
                        if i == 0 and total_points >= 500 and not purchased_boxes[i]:
                            total_points -= 500
                            purchased_boxes[i] = True
                            box = pygame.Surface((box_width, box_height))
                            box.fill(GREY)
                            text = font.render('Purchased', True, BLACK)
                            box.blit(text, (box_width // 2 - text.get_width() // 2, box_height - text.get_height()))
                            boxes[i] = box
                        if i == 0:
                            continue
                
        pygame.display.update()

    return back_to_death_screen

if __name__ == "__main__":
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    total_points = 0
    shop_gui(screen, total_points)