import pygame
import sys
import sequence_alignment

pygame.init()
screen = pygame.display.set_mode((1500, 800))
pygame.display.set_caption('Sequence Alignment')
COLOR_INACTIVE = pygame.Color('lightskyblue3')
COLOR_ACTIVE = pygame.Color('dodgerblue2')
DARKBLUE = (0, 101, 178)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
INTERMEDIARYORANGE = (255, 154, 0)
WHITE = (255, 255, 255)
FONT = pygame.font.Font(None, 32)


class InputBox:

    def __init__(self, x, y, w, h, text='', desc=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.label_input = FONT.render(desc, True, DARKBLUE)
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pygame.KEYDOWN:
            if self.active:
                # if event.key == pygame.K_RETURN:
                #    print(self.text)
                #    self.text = ''
                if event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                elif event.key != pygame.K_RETURN and event.key != pygame.K_TAB and len(self.text) < 18:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = FONT.render(self.text, True, self.color)

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 2)

        screen.blit(self.label_input, (self.rect.x, self.rect.y - 30))

def draw_solution(screen, matrix, penalty, sequence_a, sequence_b, solution_a, solution_b):
    screen.blit(FONT.render('Mismatch = 3', True, INTERMEDIARYORANGE), (20, 20))
    screen.blit(FONT.render('GAP = 2', True, INTERMEDIARYORANGE), (20, 50))

    screen.blit(FONT.render('Penalty', True, DARKBLUE), (20, 80))
    screen.blit(FONT.render(str(penalty), True, RED), (32, 110))

    screen.blit(FONT.render('Sequence Alignment', True, DARKBLUE), (20, 140))
    
    x = 0
    for word in solution_a:
        pygame.draw.rect(screen, WHITE, (20 + x, 170, 20, 30))
        screen.blit(FONT.render(word, False, RED), (23 + x, 170))
        x += 20

    x = 0
    for word in solution_b:
        pygame.draw.rect(screen, WHITE, (20 + x, 200, 20, 30))
        screen.blit(FONT.render(word, False, RED), (23 + x, 200))
        x += 20
    
    pygame.draw.rect(screen, WHITE, (600, 20, 40, 30))
    screen.blit(FONT.render(sequence_alignment.GAP_CHARACTER, False, RED), (610, 22))
    x = 0
    for word in sequence_b:
        pygame.draw.rect(screen, WHITE, (640 + x, 20, 40, 30))
        screen.blit(FONT.render(word, False, RED), (650 + x, 22))
        x += 40
    
    pygame.draw.rect(screen, WHITE, (560, 20, 40, 30))
    pygame.draw.rect(screen, WHITE, (560, 50, 40, 30))
    screen.blit(FONT.render(sequence_alignment.GAP_CHARACTER, False, RED), (570, 52))
    y = 0
    for word in sequence_a:
        pygame.draw.rect(screen, WHITE, (560, 80 + y, 40, 30))
        screen.blit(FONT.render(word, False, RED), (570, 83 + y))
        y += 30

    y = 0
    for i in range(len(matrix)):
        x = 0
        for j in range(len(matrix[0])):
            pygame.draw.rect(screen, WHITE, (600 + x, 50 + y, 40, 30))
            screen.blit(FONT.render(str(matrix[i][j]), False, RED), (610 + x, 53 + y))
            x += 40
        y += 30

def main():
    clock = pygame.time.Clock()
    input_box1 = InputBox(100, 100, 140, 32, '', 'Sequence A')
    input_box2 = InputBox(100, 300, 140, 32, '', 'Sequence B')
    input_boxes = [input_box1, input_box2]
    done = False
    close = False

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_ESCAPE]:
                pygame.quit()
                sys.exit()
            if pygame.key.get_pressed()[pygame.K_RETURN] and len(input_box1.text) > 0 and len(input_box2.text) > 0:
                done = True
            for box in input_boxes:
                box.handle_event(event)

        for box in input_boxes:
            box.update()

        screen.fill((30, 30, 30))
        for box in input_boxes:
            box.draw(screen)

        screen.blit(FONT.render('Press Enter to Run Sequence Alignment', True, RED), (550, 380))
        screen.blit(FONT.render('Press ESC to Quit', True, RED), (650, 420))

        pygame.display.flip()
        clock.tick(30)

    if done:
        screen.fill(BLACK)
        sequence_a = input_box1.text
        sequence_b = input_box2.text
        print(sequence_a)
        print(sequence_b)

        matrix, penalty = sequence_alignment.build_solution(sequence_a, sequence_b)
        solution_a, solution_b = sequence_alignment.find_solution(matrix, sequence_a, sequence_b)

    while not close:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_ESCAPE]:
                close = True
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    close = False
                    done = False
                    main()
        draw_solution(screen, matrix, penalty, sequence_a, sequence_b, solution_a, solution_b)
        screen.blit(FONT.render('Press R to Retry', True, RED), (20, 380))
        screen.blit(FONT.render('Press ESC to Quit', True, RED), (20, 420))
        pygame.display.flip()

if __name__ == '__main__':
    main()
    pygame.quit()