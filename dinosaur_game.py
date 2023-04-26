import pygame
import random

pygame.init()

WIDTH, HEIGHT = 800, 200

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Dinosaur Game')

dino_img = pygame.image.load('dino.png')
cactus_img = pygame.image.load('cactus.png')

scaled_dino_width, scaled_dino_height = 64, 64
scaled_cactus_width, scaled_cactus_height = 32, 64

dino_img = pygame.transform.scale(dino_img, (scaled_dino_width, scaled_dino_height))
cactus_img = pygame.transform.scale(cactus_img, (scaled_cactus_width, scaled_cactus_height))

dino_x, dino_y = 50, HEIGHT - dino_img.get_height()
dino_vel_y = 0
jump = False

cactus_x = WIDTH
cactus_y = HEIGHT - cactus_img.get_height()

score = 0
font = pygame.font.Font(None, 36)

def draw_dino():
    screen.blit(dino_img, (dino_x, dino_y))

def draw_cactus():
    screen.blit(cactus_img, (cactus_x, cactus_y))

def draw_score():
    text = font.render(f'Score: {score}', True, BLACK)
    screen.blit(text, (10, 10))

def draw_game_over(final_score):
    font_big = pygame.font.Font(None, 72)
    text_game_over = font_big.render('You Died', True, BLACK)
    text_final_score = font.render(f'Final Score: {final_score}', True, BLACK)
    text_respawn = font.render('Press Space to Restart', True, BLACK)

    screen.blit(text_game_over, (WIDTH // 2 - text_game_over.get_width() // 2, HEIGHT // 3 - text_game_over.get_height() // 2))
    screen.blit(text_final_score, (WIDTH // 2 - text_final_score.get_width() // 2, HEIGHT // 2 - text_final_score.get_height() // 2))
    screen.blit(text_respawn, (WIDTH // 2 - text_respawn.get_width() // 2, HEIGHT * 2 // 3 - text_respawn.get_height() // 2))

def reset_game():
    global cactus_x, score
    cactus_x = WIDTH
    score = 0

def main():
    global dino_y, dino_vel_y, jump, cactus_x, score

    clock = pygame.time.Clock()
    game_over = False

    background = pygame.Surface(screen.get_size())
    background.fill(WHITE)

    while True:
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            if not game_over:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and not jump:
                        jump = True
                        dino_vel_y = -15

                if jump:
                    dino_y += dino_vel_y
                    dino_vel_y += 1
                    if dino_y >= HEIGHT - dino_img.get_height():
                        dino_y = HEIGHT - dino_img.get_height()
                        jump = False

                    cactus_x -= 5
                    if cactus_x < -cactus_img.get_width():
                        cactus_x = WIDTH
                        score += 1

                    if dino_x + dino_img.get_width() > cactus_x and \
                            dino_x < cactus_x + cactus_img.get_width() and \
                            dino_y + dino_img.get_height() > cactus_y:
                        game_over = True

                screen.blit(background, (0, 0))
                draw_dino()
                draw_cactus()
                draw_score()

            else:
                draw_game_over(score)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        reset_game()
                        game_over = False
                        dino_y = HEIGHT - dino_img.get_height()
                        jump = False
                        cactus_x = WIDTH

        pygame.display.update()

if __name__ == '__main__':
    main()