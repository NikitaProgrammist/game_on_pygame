import pygame
from constants import sc


def menu(sc):
    finput = False
    text = ''
    tick = 30
    pygame.display.set_caption('Меню Игры')
    location_buttons = [pygame.Rect(100 + 200 * i, 100, 180, 100) for i in range(3)]
    current_screen = 'location'
    done = False
    while not done:
        sc.fill((255, 255, 255))
        for i, btn in enumerate(location_buttons, 1):
            pygame.draw.rect(sc, (0, 0, 0), btn)
            sc.blit(pygame.image.load(f'img/sky{i}.png'), (btn.x, btn.y))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if current_screen == 'location':
                    for i, btn in enumerate(location_buttons, 1):
                        if btn.collidepoint(event.pos):
                            location = i
                            current_screen = 'labyrinth'
                            done = True
        pygame.display.flip()
    clock = pygame.time.Clock()
    while True:
        sc.fill((255, 255, 255))
        rect = pygame.Rect(20, 400, 250, 70)
        pygame.draw.rect(sc, (0, 0, 0), rect, 1)
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                finput = True
            if finput and event.type == pygame.KEYDOWN:
                text = text.replace('|', '')
                tick = 30
                if event.key == pygame.K_RETURN:
                    text = text.replace('|', '')
                    finput = False
                    size = text.split(', ')
                    if len(size) == 2 and size[0].isdigit() and size[1].isdigit() and 5 <= int(
                            size[0]) <= 100 and 5 <= int(size[1]) <= 100:
                        return int(size[0]), int(size[1]), location
                elif event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                else:
                    if len(text) < 8:
                        text += event.unicode
                text += '|'
        if finput:
            tick -= 1
            if tick == 0:
                text = text.replace('|', '')
            if tick == -30:
                text += '|'
                tick = 30
        if len(text):
            font = pygame.font.Font(None, 50)
            text_surface = font.render(text, True, (0, 0, 0))
            text_rect = text_surface.get_rect()
            text_rect.topleft = (rect.x, rect.y)
            sc.blit(text_surface, text_rect)
        pygame.display.flip()
        clock.tick(60)

a, b, tex = menu(sc)