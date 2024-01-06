import pygame


def menu(sc):
    finput = False
    text = ''
    tick = 30
    pygame.display.set_caption('Меню Игры')
    font = pygame.font.Font(None, 50)
    text_surface = font.render('Выберите локацию, на которой вы хотите проходить лабиринт.', True, (0, 0, 0))
    text_rect = text_surface.get_rect()
    text_rect.topleft = (sc.get_size()[0] // 2 - text_rect.width // 2, 100)
    location_buttons = [pygame.Rect(100 + 200 * i, 400, 180, 100) for i in range(4)] + [pygame.Rect(100 + 200 * i, 600, 180, 100) for i in range(4)]
    run = True
    while run:
        sc.fill((255, 255, 255))
        sc.blit(text_surface, text_rect)
        for i, btn in enumerate(location_buttons, 1):
            pygame.draw.rect(sc, (0, 0, 0), btn)
            sc.blit(pygame.image.load(f'img/wall{i}.png'), (btn.x, btn.y))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i, btn in enumerate(location_buttons, 1):
                    if btn.collidepoint(event.pos):
                        location = i
                        run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    quit()
        pygame.display.flip()
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 50)
    text_surface_2 = font.render('Укажите размеры лабиринта через запятую.', True, (0, 0, 0))
    text_rect_2 = text_surface_2.get_rect()
    text_rect_2.topleft = (sc.get_size()[0] // 2 - text_rect_2.width // 2, 100)
    font = pygame.font.Font(None, 50)
    text_surface_3 = font.render('Они должны лежать в диапазоне от 5 до 100. (например: 10, 10)', True, (0, 0, 0))
    text_rect_3 = text_surface_3.get_rect()
    text_rect_3.topleft = (sc.get_size()[0] // 2 - text_rect_3.width // 2, 200)
    while True:
        sc.fill((255, 255, 255))
        sc.blit(text_surface_2, text_rect_2)
        sc.blit(text_surface_3, text_rect_3)
        rect = pygame.Rect((sc.get_size()[0] - 200) // 2, 400, 200, 70)
        pygame.draw.rect(sc, (0, 0, 0), rect, 1)
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                finput = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    quit()
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
                    continue
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
            text_surface_4 = font.render(text, True, (0, 0, 0))
            text_rect_4 = text_surface_3.get_rect()
            text_rect_4.topleft = (rect.x + 20, rect.y + 15)
            sc.blit(text_surface_4, text_rect_4)
        pygame.display.flip()
        clock.tick(60)