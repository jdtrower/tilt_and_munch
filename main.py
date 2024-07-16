from codex import *

# Initialize global variables
bg_color = (0, 0, 0)
fg_color = (255, 255, 255)
comp_color = (0, 0, 255)

# Generate a randomly generated RGB color
def random_color():
    red = random.randrange(0, 256)
    green = random.randrange(0, 256)
    blue = random.randrange(0, 256)
    return red, green, blue # returns a tuple in (r, g, b) format

# Function used to calculate the relative luminance of a color
def luminance(color):
    # Break the tuple into it's individual parts and assign them to variables for r, g, and b
    r, g, b = color

    # Normalize r, g, and b values to [0,1] range
    r /= 255.0
    g /= 255.0
    b /= 255.0

    # Convert sRGB to linear RGB
    # The follow code is written using ternary expressions which makes more concise code,
    # but that conciseness comes at the expense of easy readability of the code
    r = r / 12.92 if r <= 0.04045 else ((r + 0.055) / 1.055) ** 2.4
    g = g / 12.92 if g <= 0.04045 else ((g + 0.055) / 1.055) ** 2.4
    b = b / 12.92 if b <= 0.04045 else ((b + 0.055) / 1.055) ** 2.4

    # The above code for the red value can be written as the following:
    # if r <= 0.04045:
    #     r = r / 12.92
    # else:
    #     ((r + 0.055) / 1.055) ** 2.4

    # Calculate the relative luminance of a color and return it to the function call
    return 0.2126 * r + 0.7152 * g + 0.0722 * b

# Determine the best text color based on the relative luminance of the background color
def text_color(background_color):
    # Set colors white and black as tuples.
    white = (255, 255, 255)
    black = (0, 0, 0)

    # Calculate the relative luminance of our background color, white, and black
    bg_luminance = luminance(background_color)
    white_luminance = luminance(white)
    black_luminance = luminance(black)

    # Calculate the contrast ratio between white and the background color
    contrast_with_white = (white_luminance + 0.05) / (bg_luminance + 0.05)

    # Calculate the contrast ratio between the background color and black
    contrast_with_black = (bg_luminance + 0.05) / (black_luminance + 0.05)

    # Return the color with the highest contrast ratio
    if contrast_with_white >= 7:
        return white
    elif contrast_with_black >= 7:
        return black
    else:
        # If both contrasts are below 7:1, generate a new background color and then re-test for the text color
        # This ensures that there is always sufficient contrast between foreground and background colors
        bg_color = (random_color())
        fg_color = text_color(bg_color)

# Find a complementary color to the background color
def find_complementary_color(bg_color):
    # Break the tuple into it's individual parts and assign them to variables for r, g, and b
    r, g, b = bg_color

    # Invert each component by subtracting it from 255
    comp_r = 255 - r
    comp_g = 255 - g
    comp_b = 255 - b

    # return the complementary color
    return (comp_r, comp_g, comp_b)

# Draw a dot on screen at an (x, y) coordinate
def generate_random_dot():
    global dot_x, dot_y, comp_color

    # Randomly generate an x and y position for the dot
    dot_x = random.randint(5, SCREEN_WIDTH - 5)
    dot_y = random.randint(5, SCREEN_HEIGHT - 5)

    # Check if generated dot is located in the corners of the screen where the ball can't reach
    # If so, generate a new random dot in a new location on screen
    if (dot_x < 20 and dot_y < 20) or (dot_x > 220 & dot_y < 20) or\
    (dot_x < 20 & dot_y > 220) or (dot_x > 220 and dot_y > 220):
        generate_random_dot()

    # Draw the dot on screen
    display.fill_circle(dot_x, dot_y, DOT_RADIUS, comp_color)

# Turn off all pixels and LEDs
def clear_lights():
    # Turn all pixels and LEDs off
    num_pixels = 4
    num_leds = 6
    for i in range(num_pixels):
        pixels.set(i, (0, 0, 0))
    for j in range(num_leds):
        leds.set(j, False)

# Setup the welcome screen
def welcome_screen():
    display.clear()
    bg_color = (random_color())
    txt_color = text_color(bg_color)
    display.fill(bg_color)
    display.draw_text("Tilt", x=85, y=10, scale=3, color=txt_color, background=bg_color)
    display.draw_text("&", x=110, y=40, scale=4, color=txt_color, background=bg_color)
    display.draw_text("Munch", x=80, y=75, scale=3, color=txt_color, background=bg_color)
    display.draw_text("Player 1: Press A", x=15, y=110, scale=2, color=txt_color, background=bg_color)
    display.draw_text("Player 2: Press B", x=15, y=130, scale=2, color=txt_color, background=bg_color)
    display.draw_text("Tilt device to", x=35, y=155, scale=2, color=txt_color, background=bg_color)
    display.draw_text("munch on yummy dots", x=5, y=175, scale=2, color=txt_color, background=bg_color)
    display.draw_text("but avoid the edge", x=15, y=195, scale=2, color=txt_color, background=bg_color)
    display.draw_text("of the screen", x=40, y=215, scale=2, color=txt_color, background=bg_color)

# Setup the exit program screen
def exit_program():
    display.clear()
    clear_lights()
    bg_color = (random_color())
    txt_color = text_color(bg_color)
    display.fill(bg_color)
    display.draw_text("Thank you", x=40, y=20, color=fg_color, background=bg_color, scale=3)
    display.draw_text("for playing!", x=15, y=50, color=fg_color, background=bg_color, scale=3)
    display.draw_text("Designed &", x=60, y=120, color=fg_color, background=bg_color, scale=2)
    display.draw_text("Created by", x=60, y=150, color=fg_color, background=bg_color, scale=2)
    display.draw_text("David Trower", x=15, y=180, color=fg_color, background=bg_color, scale=3)

# Display welcome screen to start the game
welcome_screen()

# Main loop
while True:
    # Check if Down Button is pressed to exit the game
    if buttons.was_pressed(BTN_D):
        break

# Call the exit program function to clean up and shut down the program
exit_program()