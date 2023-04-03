import pygame

# Initialize Pygame
pygame.init()

# Set up the display
size = (400, 300)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("List Display")

# Define the font and font size
font = pygame.font.SysFont('Arial', 20)

# Define the colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Define the list
my_list = ["Hello", "World"]


# Define a function to display the list
def display_list():
    screen.fill(WHITE)
    y = 50
    for item in my_list:
        text = font.render(item, True, BLACK)
        screen.blit(text, (50, y))
        y += 30
    pygame.display.update()


# Call the display_list function to initially display the list
display_list()

# Main loop
running = True
while running:
    # Check for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_a:
                # Add an item to the list
                my_list.append("Item added")
                display_list()

# Quit Pygame
pygame.quit()
