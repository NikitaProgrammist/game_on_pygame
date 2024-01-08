import pygame
import sqlite3
from buttons import Button


def table(sc):
    pass


def start_game(sc):
    font = pygame.font.Font(None, 50)
    button_1 = Button(sc.get_size()[0] // 2 - 125, 200, 250, 70, font, 'новая игра')
    button_2 = Button(sc.get_size()[0] // 2 - 125, 300, 250, 70, font, 'рекорды')
    button_3 = Button(sc.get_size()[0] // 2 - 125, 400, 250, 70, font, 'выйти из игры')
    text_surface = font.render('затерянный в лабиринте', True, (0, 0, 0))
    text_rect = text_surface.get_rect()
    text_rect.topleft = (sc.get_size()[0] // 2 - text_rect.width // 2, 100)
    clock = pygame.time.Clock()
    while True:
        sc.fill((255, 255, 255))
        sc.blit(text_surface, text_rect)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    quit()
        flag_1 = button_1.process()
        flag_2 = button_2.process()
        flag_3 = button_3.process()
        if flag_1:
            return True
        if flag_2:
            table(sc)
        if flag_3:
            quit()
        pygame.display.flip()
        clock.tick(60)


def game_init(sc):
    finput = False
    text = ''
    tick = 30
    pygame.display.set_caption('Меню Игры')
    font = pygame.font.Font(None, 50)
    text_surface = font.render('Выберите локацию, на которой вы хотите проходить лабиринт.', True, (0, 0, 0))
    text_rect = text_surface.get_rect()
    text_rect.topleft = (sc.get_size()[0] // 2 - text_rect.width // 2, 100)
    location_buttons = [pygame.Rect(sc.get_size()[0] // 2 - 580 + 300 * i, 250, 250, 250) for i in range(4)] + [pygame.Rect(sc.get_size()[0] // 2 - 580 + 300 * i, 550, 250, 250) for i in range(4)]
    run = True
    while run:
        sc.fill((255, 255, 255))
        sc.blit(text_surface, text_rect)
        for i, btn in enumerate(location_buttons, 1):
            pygame.draw.rect(sc, (0, 0, 0), btn)
            sc.blit(pygame.image.load(f'img/location{i}.png'), (btn.x, btn.y))
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
            if tick <= 0:
                text = text[:-1] if text.endswith('|') else text + '|'
                tick = 30
        if text:
            font = pygame.font.Font(None, 50)
            text_surface_4 = font.render(text, True, (0, 0, 0))
            text_rect_4 = text_surface_3.get_rect()
            text_rect_4.topleft = (rect.x + 20, rect.y + 15)
            sc.blit(text_surface_4, text_rect_4)
        pygame.display.flip()
        clock.tick(60)


def menu(sc):
    font = pygame.font.Font(None, 50)
    font_1 = pygame.font.Font(None, 75)
    button_0 = Button(sc.get_size()[0] // 2 - 175, 200, 350, 70, font, 'продолжить игру')
    button_1 = Button(sc.get_size()[0] // 2 - 175, 300, 350, 70, font, 'новая игра')
    button_2 = Button(sc.get_size()[0] // 2 - 175, 400, 350, 70, font, 'рекорды')
    button_3 = Button(sc.get_size()[0] // 2 - 175, 500, 350, 70, font, 'выйти из игры')
    text_surface = font_1.render('затерянный в лабиринте', True, (0, 0, 0))
    text_rect = text_surface.get_rect()
    text_rect.topleft = (sc.get_size()[0] // 2 - text_rect.width // 2, 100)
    clock = pygame.time.Clock()
    pygame.mouse.set_visible(True)
    while True:
        pygame.draw.rect(sc, (255, 255, 255), (sc.get_size()[0] // 2 - text_rect.width // 2, 100, *text_surface.get_rect()[2:]))
        sc.blit(text_surface, text_rect)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
        flag_0 = button_0.process()
        flag_1 = button_1.process()
        flag_2 = button_2.process()
        flag_3 = button_3.process()
        if flag_0:
            return
        if flag_1:
            return True
        if flag_2:
            table(sc)
        if flag_3:
            quit()
        pygame.display.flip()
        clock.tick(60)


def win(sc, minutes, seconds, a, b, tex):
    con = sqlite3.connect('records.sqlite')
    cur = con.cursor()
    result = cur.execute(f"""SELECT * FROM record WHERE width = {a} AND height = {b}""").fetchone()
    if not result:
        cur.execute(f"""INSERT INTO record (width, height, minutes, seconds, location) VALUES 
            ({a}, {b}, {minutes}, {seconds}, {tex})""")
    elif result and (int(result[-3]) > minutes or (int(result[-3]) == minutes and int(result[-2]) > seconds)):
        cur.execute(f"""REPLACE INTO record (id, width, height, minutes, seconds, location) VALUES 
            ({result[0]}, {a}, {b}, {minutes}, {seconds}, {tex})""")
    con.commit()
    con.close()
    font = pygame.font.Font(None, 75)
    text_surface = font.render('Поздравляю!', True, (255, 255, 255))
    text_rect = text_surface.get_rect()
    text_rect.topleft = (sc.get_size()[0] // 2 - text_rect.width // 2, sc.get_size()[1] // 2 - text_rect.height // 2 - 200)
    text_surface_1 = font.render(f'Вы прошли лабиринт {a} на {b} за {minutes}: {seconds}', True, (255, 255, 255))
    text_rect_1 = text_surface.get_rect()
    text_rect_1.topleft = (sc.get_size()[0] // 2 - text_rect.width // 2 - 250, sc.get_size()[1] // 2 - text_rect.height // 2)
    while True:
        sc.blit(text_surface, text_rect)
        sc.blit(text_surface_1, text_rect_1)
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                return True
        pygame.display.flip()