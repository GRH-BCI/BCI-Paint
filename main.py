from utils import *
import os
import random

def draw(win, dir_clock, buttons, size_buttons, brush_speed_slider, clock_speed_slider, brush, colour_picker, theta):
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

    pygame.draw.rect(win, WHITE, (0, 0, TOOLBAR_HEIGHT, win.get_height()))

    x, y = pygame.mouse.get_pos()
    if x < TOOLBAR_HEIGHT:
        # Create toolbar headings
        heading_font = get_font(18)
        brush_colour_heading = heading_font.render("Brush Colour", 1, BLACK)
        brush_size_heading = heading_font.render("Brush Size", 1, BLACK)
        mode_heading = heading_font.render("Mode", 1, BLACK)
        brush_speed_heading = heading_font.render("Brush Speed", 1, BLACK)
        clock_speed_heading = heading_font.render("Clock Speed", 1, BLACK)
        # Draw the toolbar headings
        win.blit(brush_colour_heading, (10, 320))
        win.blit(brush_size_heading, (10, 580))
        win.blit(mode_heading, (10, 680))
        win.blit(brush_speed_heading, (200, 580))
        win.blit(clock_speed_heading, (10, 10))

        for button in buttons.values():
            # print(button)
            button.draw(win)

        for button in size_buttons:
            button.draw(win)

        colour_picker.update()
        colour_picker.draw(win)

        brush_speed_slider.update()
        brush_speed_slider.draw(win)

        clock_speed_slider.update()
        clock_speed_slider.draw(win)

    # Draw direction animation
    dir_clock.draw(win, brush.colour, theta)

    pygame.display.update()


def main():
    run = True
    clock = pygame.time.Clock()

    icon = pygame.image.load(os.path.join("Assets", "paint-palette.png"))
    pygame.display.set_icon(icon)

    theta = 0
    pause = False
    rainbow = False
    hue = 0
    mode = "Casual"
    move =  False
    counter = 0

    # Set the window size to the size of the device screen if possible otherwise use the default width and height
    display_info = pygame.display.Info()

    if display_info.current_h < 0 or display_info.current_w < 0:
        WIN = pygame.display.set_mode((DEFAULT_WIDTH, DEFAULT_HEIGHT), pygame.RESIZABLE)
    else:
        WIN = pygame.display.set_mode((display_info.current_w, display_info.current_h* 0.90), pygame.RESIZABLE)
    
    pygame.display.set_caption("Paint Program")

    WIN.fill(BG_COLOUR)

    dir_clock = Clock(TOOLBAR_HEIGHT//2, WIN.get_height()*(1/5) + PADDING, WIN.get_height()*(1/5))

    # Create the colour buttons and save button
    h = WIN.get_height()*(1/15)
    w = WIN.get_height()*(1/15)

    black = Button(0 + PADDING, dir_clock.bottom + PADDING, w, h, BLACK, selected=True)
    white = Button(black.right + PADDING, dir_clock.bottom + PADDING, w, h, WHITE)
    red = Button(white.right + PADDING, dir_clock.bottom + PADDING, w, h, RED)
    yellow = Button(red.right + PADDING, dir_clock.bottom + PADDING, w, h, YELLOW)
    blue = Button(yellow.right + PADDING, dir_clock.bottom + PADDING, w, h, BLUE)

    orange = Button(0 + PADDING, black.bottom + PADDING, w, h, ORANGE)
    green = Button(orange.right + PADDING, white.bottom + PADDING, w, h, GREEN)
    purple = Button(green.right + PADDING, red.bottom + PADDING, w, h, PURPLE)
    multi = Button(purple.right + PADDING, yellow.bottom + PADDING, w, h, WHITE, text="Multi")
    save = Button(multi.right + PADDING, blue.bottom + PADDING, w, h, WHITE, text="Save")

    casual = Button(0 + PADDING, 710, 2*w, h, WHITE, selected=True, text="Casual")
    game = Button(casual.right + PADDING, 710, 2*w, h, WHITE, text="Game")

    buttons = {
        "Black": black,
        "White": white,
        "Red": red,
        "Yellow": yellow,
        "Blue": blue,
        "Orange": orange,
        "Green": green,
        "Purple": purple,
        "Multi": multi,
        "Save": save,
        "Casual": casual,
        "Game": game
    }

    # Create the colour picker
    colour_picker = ColorPicker(0, 470)

    size_buttons = [
        RoundButton(10 + BrushSize.LARGE.value, 610 + BrushSize.LARGE.value, BrushSize.LARGE.value, BLACK, selected=False),
        RoundButton(10 + BrushSize.LARGE.value*2 + BrushSize.MEDIUM.value + 10, 610 + BrushSize.LARGE.value, BrushSize.MEDIUM.value, BLACK, selected=True),
        RoundButton(10 + BrushSize.LARGE.value*2 + BrushSize.MEDIUM.value*2 + BrushSize.SMALL.value + 2*10, 610 + BrushSize.LARGE.value, BrushSize.SMALL.value, BLACK, selected=False)
    ]
    
    brush_speed_slider = SliderButton(220, 630, 90, 20, 100, 5, 5)
    clock_speed_slider = SliderButton(25, 50, 40, 10, 1, 0, 0.5)

    brush = Brush((WIN.get_width() - TOOLBAR_HEIGHT)/2 + TOOLBAR_HEIGHT, WIN.get_height()/2, BrushSize.MEDIUM.value, BLACK)

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.VIDEORESIZE:
                WIN.fill((255, 255, 255))

                dir_clock.r = WIN.get_height()*(1/5)
                dir_clock.y = dir_clock.r + PADDING
                dir_clock.x = TOOLBAR_HEIGHT//2
                dir_clock.update()

                for id, button in buttons.items():
                    if id == "Game" or id == "Casual":
                        button.width = WIN.get_height()*(2/15)
                        button.height = WIN.get_height()*(1/15)
                    else:
                        button.width = WIN.get_height()*(1/15)
                        button.height = WIN.get_height()*(1/15)

                        if id == "Black" or id == "White" or id == "Red" or id == "Yellow" or id == "Blue":
                            button.y = dir_clock.bottom + PADDING
                        else:
                            button.y = buttons["Black"].bottom + PADDING

                    button.update()

            if pygame.mouse.get_pressed()[0]: # LEFT MOUSE BUTTON
                pos = pygame.mouse.get_pos()

                # Check if one of the colour buttons or save button was clicked
                for button in buttons.values():
                    if not button.clicked(pos):
                        if button.text == "Save" or (button.text == "Multi" and rainbow == False):
                            button.selected = False
                        
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

                    elif button.text == "Multi":
                        brush.colour.hsla = (0, 100, 50, 100)
                        hue = 0
                        rainbow = True

                    elif button.text == "Game":
                        mode = "Game"
                        button.selected = True
                        buttons["Casual"].selected = False

                    elif button.text == "Casual":
                        mode = "Casual"
                        button.selected = True
                        buttons["Game"].selected = False

                    else:
                        brush.colour = pygame.Color(button.colour)
                        rainbow = False

                # After checking for a colour change indicate which colour was selected
                for button in buttons.values():
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
                rainbow = False

            # if event.type == PAUSE_ROTATION:
            #     pause = True

        keys_pressed = pygame.key.get_pressed()

        # If game mode is selected and the w key is pressed start the movement counter
        if mode == "Game" and keys_pressed[pygame.K_w]:
            move = True
            counter = 0
            brush.vel = brush_speed_slider.value
        elif mode == "Casual":
            brush.vel = brush_speed_slider.value

            # for i in range(0, 100):
            #     xo = random.gauss(0, 25)
            #     yo = random.gauss(0, 25)
            #     pygame.draw.circle(WIN, brush.colour, (brush.x + xo, brush.y + yo), 1)

            #     a = random.random()
            #     if a > 0.9:
            #         for i in range (0, 40):
            #             pygame.draw.circle(WIN, brush.colour, (brush.x + xo, brush.y + yo + i), 1)


        # In game mode the brush should continuously move for 300 iterations of the loop after the w key is pressed
        if move == True:    
            counter += 1
    
        if counter > 300:
            move = False
            counter = 0
            brush.vel = 5
        # The brush should slow down over time
        elif counter > 150:
            brush.x_vel = brush.x_vel * 0.99
            brush.y_vel = brush.y_vel * 0.99

        brush.handle_movement(WIN, keys_pressed, theta, mode, move)

        theta = (theta + clock_speed_slider.value) % 360

        # If the multicolor button is selected consistently change the hue
        if rainbow:
            hue = (hue + 1) % 360
            brush.colour.hsla = (hue, 100, 50, 100)

        # if not pause:
        #     theta = (theta + 0.5) % 360
        
        # pause = False

        draw(WIN, dir_clock, buttons, size_buttons, brush_speed_slider, clock_speed_slider, brush, colour_picker, theta)

    pygame.quit()

if __name__ == "__main__":
    main()