import pygame
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


# class Label2(pygame.font):
#     def __init__(self, text):
#         super().init()
#         super().Font('freesansbold.ttf', 15)
#         self.text = text
#
#     def update_text(self, text):
#         self.text = text
#
#     def render(self):
#         return self.Font(self.text, True, WHITE, BLACK)
# class Label:
#     def __init__(self, text, x, y):
#         self.x, self.y = x, y
#         self.text = text
#         pygame.font.init()
#         self.font = pygame.font.Font('freesansbold.ttf', 15)
#         self.text_surface = font.render(self.text, True, WHITE, BLACK)
#
#     def draw(self):
#         screen.blit(self.surface, (self.x, self.y))
#
#     def update_text(self, text):
#         self.text_surface = font.render(text, True, WHITE, BLACK)
#
#     def get_text_surface(self):
#         return self.text_surface


class Window:
    def __init__(self, x: int=400, y: int=300):

        pygame.init()

        self.X, self.Y = x, y
        self.screen = pygame.display.set_mode((self.X, self.Y))
        pygame.display.set_caption("List Display")

        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)

        self.text_list = texts

        self.screen.fill(self.BLACK)

        self.running = True
        self.change = False

    def _display_list(self, text_list):
        # screen.fill(self.WHITE)
        # print('got here')
        y = 50
        pygame.font.init()
        for item in text_list:
            font = pygame.font.Font('freesansbold.ttf', 15)
            text = font.render(item, True, WHITE)
            self.screen.blit(text, (10, y))
            y += 30
        pygame.display.update()

    def run(self, text_list):
        print(text_list)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        self._display_list(text_list)
        pygame.display.update()


if __name__ == '__main__':
    # pygame.init()
    # text_surface = Label2('ttt')
    # running = True
    # while running:
    #     self.screen.blit(text_surface, (200, 150))
    #     text_surface.update_text('ppp')
    #     for event in pygame.event.get():
    #         if event.type == pygame.QUIT:
    #             pygame.quit()
    #         elif event.type == pygame.KEYDOWN:
    #             if event.key == pygame.K_ESCAPE:
    #                 pygame.quit()
    #     pygame.display.update()
    texts = ['a', 'b', 'c']
    win = Window()
    win.run(texts)
    texts = ['b', 'c', 'd']
    win.run(texts)
