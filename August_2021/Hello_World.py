import pygame
from time import sleep

color_list = [(255, 0, 0), (255, 128, 0), (255, 255, 0), (128, 255, 0), (0, 255, 0), (0, 255, 128), (0, 255, 255),
              (0, 128, 255), (0, 0, 255), (127, 0, 255), (255, 0, 255), (255, 0, 127)]
pygame.init()
pygame.font.init()
FONT_SIZE = 100
font = pygame.font.SysFont('Comic Sans', FONT_SIZE)

WIDTH, HEIGHT = 900, 700
window = pygame.display.set_mode((WIDTH, HEIGHT))
background = pygame.rect.Rect(0, 0, WIDTH, HEIGHT) 

sentence = 'Hello, World!'
broken_list = list(sentence)
compiled_text = ''

for i in broken_list:
    compiled_text += i


running = True
letter_graphics_list = []


def update_display():
    pygame.draw.rect(window, (0, 0, 0), background)
    for j in letter_graphics_list:
        window.blit(j.object, (j.x, j.y))
    pygame.display.flip()
    sleep(.09)


class Letters:
    def __init__(self, letter, x, y, index):
        self.text = letter
        self.x = x
        self.y = y
        self.start = y
        self.color_index = index
        self.done_moving = False
        self.visited_top = False
        self.object = font.render(self.text, False, (255, 255, 255))
        self.order = index
        self.order_constant = index

    def change_y(self):
        if self.order > 12:
            if self.color_index > 11:
                self.color_index = 0
            self.object = font.render(self.text, False, color_list[self.color_index])
            if self.y <= 0:
                self.visited_top = True

            if self.y == self.start and self.visited_top:
                self.done_moving = True
                self.visited_top = False

            elif self.visited_top:
                self.y += 50
            elif not self.visited_top:
                self.y -= 50
            self.color_index += 1
        self.order += 1


letter_pos = -1
for i in broken_list:
    letter_pos += 1
    letter_graphics_list.append(Letters(i, x=(letter_pos+1)*60, y=HEIGHT-FONT_SIZE, index=letter_pos))


while running:
    pygame.display.set_caption(compiled_text)
    for events in pygame.event.get():
        if events.type == pygame.QUIT:
            running = False
            pygame.quit()
            quit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        moving_list = letter_graphics_list.copy()

        while len(moving_list) > 0:
            for i in range(len(moving_list)):
                if moving_list[i].done_moving:
                    moving_list[i].done_moving = False
                    moving_list[i].order = moving_list[i].order_constant
                    moving_list.remove(moving_list[i])
                    break
                moving_list[i].change_y()
            update_display()

