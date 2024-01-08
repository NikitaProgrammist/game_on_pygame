from constants import *


class Button:
    def __init__(self, x, y, width, height, font, buttontext='Button', press=False):
        self.width = width
        self.height = height
        self.press = press
        self.buttonscreen = pygame.Surface((self.width, self.height))
        self.buttonrect = pygame.Rect(x, y, self.width, self.height)
        self.buttonsurface = font.render(buttontext, True, (20, 20, 20))
        self.pressed = False

    def process(self):
        pos = pygame.mouse.get_pos()
        self.buttonscreen.fill((255, 255, 255))
        if self.buttonrect.collidepoint(pos):
            self.buttonscreen.fill((100, 100, 100))
            if pygame.mouse.get_pressed()[0]:
                self.buttonscreen.fill((50, 50, 50))
                if self.press:
                    return True
                elif not self.pressed:
                    self.pressed = True
                    return True
            else:
                self.pressed = False
        self.buttonscreen.blit(self.buttonsurface, [
            self.buttonrect.width / 2 - self.buttonsurface.get_rect().width / 2,
            self.buttonrect.height / 2 - self.buttonsurface.get_rect().height / 2
        ])
        sc.blit(self.buttonscreen, self.buttonrect)
