from utils import *

WIN = pygame.display.set_mode((DEFAULT_WIDTH, DEFAULT_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Paint Program")


def draw(win, buttons, brush):
    """
    Draws all the elements on the canvas

    Parameters:
    ----------
    win: Surface
        The window to draw on
    buttons: 
        The buttons to draw
    brush:
        The paint brush to draw
    """

    brush.draw(win)

    for button in buttons:
        button.draw(win)

    pygame.display.update()


def main():
    run = True
    clock = pygame.time.Clock()

    WIN.fill(BG_COLOUR)

    # Draw the colour buttons
    button_height = 50
    button_width = 50
    button_y = DEFAULT_HEIGHT - TOOLBAR_HEIGHT/2 - button_height/2

    buttons = [
        Button(10, button_y, button_height, button_width, BLACK),
        Button(70, button_y, button_height, button_width, WHITE),
        Button(130, button_y, button_height, button_width, RED),
        Button(190, button_y, button_height, button_width, YELLOW),
        Button(250, button_y, button_height, button_width, BLUE),
        Button(310, button_y, button_height, button_width, ORANGE),
        Button(370, button_y, button_height, button_width, GREEN),
        Button(430, button_y, button_height, button_width, PURPLE),
    ]

    # Display Tool bar headings
    heading_font = get_font(16)
    text_surface = heading_font.render("Brush Colours", 1, BLACK)
    WIN.blit(text_surface, (245 - text_surface.get_width()/2, button_y - 10 - text_surface.get_height()))

    brush = Brush(DEFAULT_WIDTH/2, (DEFAULT_HEIGHT - TOOLBAR_HEIGHT)/2 - BrushSize.MEDIUM.value, BrushSize.MEDIUM.value, BLACK)
    

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if pygame.mouse.get_pressed()[0]: # LEFT MOUSE BUTTON
                pos = pygame.mouse.get_pos()

                # Check if one of the buttons was clicked
                for button in buttons:
                    if not button.clicked(pos):
                        continue

                    brush.colour = button.colour

        keys_pressed = pygame.key.get_pressed()

        brush.handle_movement(keys_pressed)

        draw(WIN, buttons, brush)

    # Save an image of the canvas before exiting
    # pygame.image.save(WIN, "screenshot.jpeg")
    pygame.quit()

if __name__ == "__main__":
    main()