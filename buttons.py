from constants import *


class Button:
    def __init__(self, x, y, width, height, font, buttonText='Button', press=False):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.press = press
        self.font = font
        self.colors = {
            'normal': '#ffffff',
            'hover': '#666666',
            'pressed': '#333333',
        }

        self.buttonscreen = pygame.Surface((self.width, self.height))
        self.buttonrect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.buttonsurface = self.font.render(buttonText, True, (20, 20, 20))

        self.pressed = False

    def process(self):
        pos = pygame.mouse.get_pos()
        self.buttonscreen.fill(self.colors['normal'])
        if self.buttonrect.collidepoint(pos):
            self.buttonscreen.fill(self.colors['hover'])
            if pygame.mouse.get_pressed()[0]:
                self.buttonscreen.fill(self.colors['pressed'])
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
