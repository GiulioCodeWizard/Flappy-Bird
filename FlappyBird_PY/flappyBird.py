"""
Dajani Giulio
Flappy Bird Game in .py
"""

# sudo pip install pygame
import pygame
import random

def main():
    bird_x, bird_y, bird_vel_y, base_x = 60, 150, 0, 0
    display, FPS, velocity = pygame.display.set_mode((288, 512)), 60, 5

    pygame.init()

    background = pygame.image.load('img/background.png')
    bird = pygame.image.load('img/bird.png')
    base = pygame.image.load('img/base.png')
    game_over = pygame.image.load('img/game_over.png')
    tube_down = pygame.image.load('img/tube.png')
    tube_up = pygame.transform.flip(tube_down, False, True)

    tube_width = tube_down.get_width()
    tube_gap = 100
    tubes = []
    tube_frequency = 90
    frame_count = 0
    points = 0
    top_scores = []

    font = pygame.font.SysFont(None, 36)

    def add_tube():
        height = random.randint(50, 250)
        tubes.append({'x': 288, 'y': height})

    def check_collision():
        for t in tubes:
            tube_x = t['x']
            tube_y = t['y']
            if bird_x + bird.get_width() > tube_x and bird_x < tube_x + tube_width:
                if bird_y < tube_y or bird_y + bird.get_height() > tube_y + tube_gap:
                    return True
        return bird_y > 400

    def show_menu():
        display.fill((0, 0, 0))
        menu_text = font.render("Top Scores", True, (255, 255, 255))
        display.blit(menu_text, (90, 50))
        for i, score in enumerate(sorted(top_scores, reverse=True)[:5]):
            score_text = font.render(f"{i + 1}. {score}", True, (255, 255, 255))
            display.blit(score_text, (90, 100 + i * 30))
        pygame.display.update()
        waiting = True
        while waiting:
            for e in pygame.event.get():
                if e.type == pygame.KEYDOWN and e.key == pygame.K_m:
                    waiting = False
                if e.type == pygame.QUIT:
                    pygame.quit()

    while True:
        bird_vel_y += 1
        bird_y += bird_vel_y

        frame_count += 1
        if frame_count % tube_frequency == 0:
            add_tube()

        tubes = [{'x': t['x'] - velocity, 'y': t['y']} for t in tubes if t['x'] > -tube_width]

        for t in tubes:
            if t['x'] + tube_width < bird_x and 'passed' not in t:
                points += 1
                t['passed'] = True

        if check_collision():
            top_scores.append(points)
            display.blit(game_over, (50, 180))
            pygame.display.update()
            pygame.time.Clock().tick(FPS)

            restart = False
            while not restart:
                for e in pygame.event.get():
                    if e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE:
                        bird_x, bird_y, bird_vel_y, base_x = 60, 150, 0, 0
                        tubes = []  # Reset tubes
                        frame_count = 0
                        points = 0
                        restart = True
                    if e.type == pygame.KEYDOWN and e.key == pygame.K_m:
                        show_menu()
                    if e.type == pygame.QUIT:
                        pygame.quit()

        display.blit(background, (0, 0))
        for tube in tubes:
            display.blit(tube_up, (tube['x'], tube['y'] - tube_up.get_height()))
            display.blit(tube_down, (tube['x'], tube['y'] + tube_gap))
        display.blit(bird, (bird_x, bird_y))
        display.blit(base, (base_x, 400))

        points_text = font.render(f"Points: {points}", True, (255, 255, 255))
        display.blit(points_text, (10, 10))

        pygame.display.update()
        pygame.time.Clock().tick(FPS)

        for e in pygame.event.get():
            if e.type == pygame.KEYDOWN and e.key == pygame.K_UP:
                bird_vel_y = -10
            if e.type == pygame.KEYDOWN and e.key == pygame.K_m:
                show_menu()
            if e.type == pygame.QUIT:
                pygame.quit()

        base_x -= velocity
        if base_x < -48:
            base_x = 0

if __name__ == '__main__':
    main()
