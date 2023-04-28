import pygame

pygame.init()

WIDTH, HEIGHT = 1200, 400

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

def shop_gui():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Dino Shop')

    running = True
    back_to_death_screen = False
    while running:
        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    back_to_death_screen = True
                    running = False

        pygame.display.update()

    return back_to_death_screen

if __name__ == "__main__":
    shop_gui()
