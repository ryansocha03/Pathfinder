'''Class file for all buttons'''
import pygame
pygame.init()

font = pygame.font.SysFont('comincsans', 25)

class Button(object):
    def __init__(self, rect, text=''):
        self.rect = rect
        self.outline = pygame.rect.Rect(self.rect.x - 2, self.rect.y - 2, self.rect.width + 4, self.rect.height + 4)
        self.active = False         #True when the button is being hovered over
        self.clicked = False        #True when the button has been clicked
        self.text = text            #The text that the button contains

    def draw(self, window):
        pygame.draw.rect(window, (0, 0, 0), self.outline)  
        #Colors the button appropriately if it is hovered over or clicked
        if self.active or self.clicked:
            pygame.draw.rect(window, (0, 0, 0), self.rect)
            text_display = font.render(self.text, 1, (255, 255, 255))
        else:
            pygame.draw.rect(window, (255, 255, 255), self.rect)
            text_display = font.render(self.text, 1, (0, 0, 0))
        window.blit(text_display, (self.rect.x + (50 - text_display.get_width() / 2), self.rect.y + (20 - text_display.get_height() / 2)))