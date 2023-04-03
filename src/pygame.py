import pygame


pygame.init()

screen = pygame.display.set_mode((400, 300))
pygame.display.set_caption("List Display")


font = pygame.font.SysFont('Arial', 20)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

my_list = ["Hello", "World"]


def display_list():
    screen.fill(WHITE)
    y = 50
    for item in my_list:
        text = font.render(item, True, BLACK)
        screen.blit(text, (50, y))
        y += 30
    pygame.display.update()


display_list()


def add_to_list(item):
    my_list.append(item)
    display_list()


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    if pygame.display.get_active():
        new_list = pygame.display.get_caption()[0]
        if new_list != str(my_list):
            display_list()


pygame.quit()

if __name__ == "__main__":
    add_to_list("New item")
