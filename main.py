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

    for button in buttons:
        button.draw(win)

    for button in size_buttons:
        button.draw(win)

    colour_picker.update()
    colour_picker.draw(win)

    # Draw direction animation
    direction_animation_y = win.get_height() - TOOLBAR_HEIGHT/2
    pygame.draw.circle(win, WHITE, (1000, direction_animation_y), 40)
    pygame.draw.circle(win, BLACK, (1000, direction_animation_y), 40, 2)
    
    r = 35
    pygame.draw.line(win, BLACK, (1000, direction_animation_y), calc_rotation(r, theta, 1000, direction_animation_y), 2)

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

    theta = 0

    # Set the window size to the size of the device screen if possible otherwise use the default width and height
    display_info = pygame.display.Info()

    if display_info.current_h < 0 or display_info.current_w < 0:
        WIN = pygame.display.set_mode((DEFAULT_WIDTH, DEFAULT_HEIGHT))
    else:
        WIN = pygame.display.set_mode((display_info.current_w, display_info.current_h* 0.9))
    
    pygame.display.set_caption("Paint Program")

    WIN.fill(BG_COLOUR)

    # Create toolbar headings
    heading_font = get_font(16)
    brush_colour_heading = heading_font.render("Brush Colour", 1, BLACK)
    brush_size_heading = heading_font.render("Brush Size", 1, BLACK)
    toolbar_text_y = WIN.get_height() - TOOLBAR_HEIGHT + 10

    # Create the colour buttons
    button_height = 50
    button_width = 50
    button_y = WIN.get_height() - (WIN.get_height() - (toolbar_text_y + brush_colour_heading.get_height()))/2 - button_height/2
    size_button_y = WIN.get_height() - (WIN.get_height() - (toolbar_text_y + brush_size_heading.get_height()))/2

    buttons = [
        Button(10, button_y, button_height, button_width, BLACK),
        Button(70, button_y, button_height, button_width, WHITE),
        Button(130, button_y, button_height, button_width, RED),
        Button(190, button_y, button_height, button_width, YELLOW),
        Button(250, button_y, button_height, button_width, BLUE),
        Button(310, button_y, button_height, button_width, ORANGE),
        Button(370, button_y, button_height, button_width, GREEN),
        Button(430, button_y, button_height, button_width, PURPLE),
        Button(1300, button_y, button_height, button_width, WHITE, "Save")
    ]

    size_buttons = [
        RoundButton(1100 + BrushSize.LARGE.value, size_button_y, BrushSize.LARGE.value, BLACK),
        RoundButton(1100 + BrushSize.LARGE.value*2 + BrushSize.MEDIUM.value + 10, size_button_y, BrushSize.MEDIUM.value, BLACK),
        RoundButton(1100 + BrushSize.LARGE.value*2 + BrushSize.MEDIUM.value*2 + BrushSize.SMALL.value + 2*10, size_button_y, BrushSize.SMALL.value, BLACK)
    ]

    # Draw the toolbar headings
    WIN.blit(brush_colour_heading, (len(buttons) * (button_width + 10)/2 - brush_colour_heading.get_width()/2, toolbar_text_y))
    WIN.blit(brush_size_heading, (1100 + (BrushSize.LARGE.value*2 + BrushSize.MEDIUM.value*2 + BrushSize.SMALL.value + 3*10)/2- brush_size_heading.get_width()/2, toolbar_text_y))

    # Create the colour picker
    colour_picker = ColorPicker(510, WIN.get_height() - TOOLBAR_HEIGHT)

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
                        painting = WIN.subsurface((0, 0, WIN.get_width(), WIN.get_height() - TOOLBAR_HEIGHT))

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

                for button in size_buttons:
                    if brush.radius != button.radius:
                        button.selected = False

            if event.type == COLOUR_CHANGE:
                brush.colour.hsla = (colour_picker.hue, colour_picker.sat, colour_picker.light, 100)

        keys_pressed = pygame.key.get_pressed()

        brush.handle_movement(WIN, keys_pressed, theta)

        theta = (theta + 1) % 360

        draw(WIN, buttons, size_buttons, brush, colour_picker, theta)

    pygame.quit()

if __name__ == "__main__":
    main()