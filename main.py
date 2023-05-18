from utils import *
import math
import os

def draw(win, buttons, size_buttons, brush, colour_picker, theta):
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

    x, y = pygame.mouse.get_pos()
    if x < TOOLBAR_HEIGHT:
        # Create toolbar headings
        heading_font = get_font(18)
        brush_colour_heading = heading_font.render("Brush Colour", 1, BLACK)
        brush_size_heading = heading_font.render("Brush Size", 1, BLACK)
        # Draw the toolbar headings
        win.blit(brush_colour_heading, (10, 320))
        win.blit(brush_size_heading, (10, 580))

        for button in buttons:
            button.draw(win)

        for button in size_buttons:
            button.draw(win)

        colour_picker.update()
        colour_picker.draw(win)
    else:
        pygame.draw.rect(win, WHITE, (0, 0, TOOLBAR_HEIGHT, win.get_height()))

    # Draw direction animation
    pygame.draw.circle(win, WHITE, (TOOLBAR_HEIGHT//2, 160), 150)
    pygame.draw.circle(win, BLACK, (TOOLBAR_HEIGHT//2, 160), 150, 15)
    
    r = 125
    pygame.draw.line(win, BLACK, (TOOLBAR_HEIGHT//2, 160), calc_rotation(r, theta, TOOLBAR_HEIGHT//2, 160), 10)

    pygame.display.update()


def calc_rotation(r, theta, x_center, y_center):
    """
    Calculates the x and y position for the end of a line at a given angle

    Parameters:
    ----------
    r: int
        The radial length of the line
    theta: int
        The angle of the line in degrees (0 represents up)
    x_center: int
        The x coordinate of the point which one end of the line is fixed and the other endpoint rotates around
    y_center: int
        The y coordinate of the point which one end of the line is fixed and the other endpoint rotates around
    """
    y = math.cos(2*math.pi*theta/360)*r
    x = math.sin(2*math.pi*theta/360)*r
    return x + x_center, -(y - y_center)


def main():
    run = True
    clock = pygame.time.Clock()

    icon = pygame.image.load(os.path.join("Assets", "paint-palette.png"))
    pygame.display.set_icon(icon)

    theta = 0
    pause = False

    # Set the window size to the size of the device screen if possible otherwise use the default width and height
    display_info = pygame.display.Info()

    if display_info.current_h < 0 or display_info.current_w < 0:
        WIN = pygame.display.set_mode((DEFAULT_WIDTH, DEFAULT_HEIGHT))
    else:
        WIN = pygame.display.set_mode((display_info.current_w, display_info.current_h* 0.90))
    
    pygame.display.set_caption("Paint Program")

    WIN.fill(BG_COLOUR)

    # Create the colour buttons and save button
    button_height = 50
    button_width = 50

    buttons = [
        Button(10, 350, button_height, button_width, BLACK),
        Button(70, 350, button_height, button_width, WHITE),
        Button(130, 350, button_height, button_width, RED),
        Button(190, 350, button_height, button_width, YELLOW),
        Button(250, 350, button_height, button_width, BLUE),
        Button(10, 410, button_height, button_width, ORANGE),
        Button(70, 410, button_height, button_width, GREEN),
        Button(130, 410, button_height, button_width, PURPLE),
        Button(190, 410, button_height, button_width, WHITE, "Save")
    ]

    # Create the colour picker
    colour_picker = ColorPicker(0, 470)

    size_buttons = [
        RoundButton(10 + BrushSize.LARGE.value, 610 + BrushSize.LARGE.value, BrushSize.LARGE.value, BLACK),
        RoundButton(10 + BrushSize.LARGE.value*2 + BrushSize.MEDIUM.value + 10, 610 + BrushSize.LARGE.value, BrushSize.MEDIUM.value, BLACK),
        RoundButton(10 + BrushSize.LARGE.value*2 + BrushSize.MEDIUM.value*2 + BrushSize.SMALL.value + 2*10, 610 + BrushSize.LARGE.value, BrushSize.SMALL.value, BLACK)
    ]

    brush = Brush(WIN.get_width()/2, (WIN.get_height() - TOOLBAR_HEIGHT)/2, BrushSize.MEDIUM.value, BLACK)

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if pygame.mouse.get_pressed()[0]: # LEFT MOUSE BUTTON
                pos = pygame.mouse.get_pos()

                # Check if one of the colour buttons or save button was clicked
                for button in buttons:
                    if not button.clicked(pos):
                        continue
                    
                    if button.text == "Save":
                        # Save an image of the canvas
                        painting = WIN.subsurface((TOOLBAR_HEIGHT, 0, WIN.get_width() - TOOLBAR_HEIGHT, WIN.get_height()))

                        # Get a unique name for the painting
                        filename = "painting.png"
                        num = 0
                        while os.path.exists(filename):
                            num += 1
                            filename = "painting_" + str(num) + ".png"
                        
                        pygame.image.save(painting, filename)

                    else:
                        brush.colour = pygame.Color(button.colour)

                # After checking for a colour change indicate which colour was selected
                for button in buttons:
                    if button.text != None:
                        continue

                    if brush.colour.r != button.colour.r or brush.colour.g != button.colour.g or brush.colour.b != button.colour.b:
                        button.selected = False

                # Check if one of the size buttons was clicked
                for button in size_buttons:
                    if not button.clicked(pos):
                        continue

                    brush.radius = button.radius

                # Indicate which size is selected
                for button in size_buttons:
                    if brush.radius != button.radius:
                        button.selected = False

            # If a change was made on the colour picker, change the brush colour to the new colour
            if event.type == COLOUR_CHANGE:
                brush.colour.hsla = (colour_picker.hue, colour_picker.sat, colour_picker.light, 100)

            if event.type == PAUSE_ROTATION:
                pause = True

        keys_pressed = pygame.key.get_pressed()

        brush.handle_movement(WIN, keys_pressed, theta)

        theta = (theta + 0.5) % 360

        # if not pause:
        #     theta = (theta + 0.5) % 360
        
        # pause = False

        draw(WIN, buttons, size_buttons, brush, colour_picker, theta)

    pygame.quit()

if __name__ == "__main__":
    main()