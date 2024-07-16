from codex import *

# Constants
SCREEN_WIDTH = 240
SCREEN_HEIGHT = 240
DOT_RADIUS = 5

# Initialize global variables
bg_color = (0, 0, 0)
fg_color = (255, 255, 255)
comp_color = (0, 0, 255)
dot_x = 0
dot_y = 0
score = 0
lives = 3
player = 0
start_game = 0

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

# Scale the accelerometer value to screen coordinates
def scale_accel_to_screen(axis, min_val, max_val, screen_dim):
    # Scale the accelerometer value
    scaled = (axis - min_val) / (max_val - min_val)
    
    # Map the scaled value to the screen coodinates
    screen_coord = int(scaled * (screen_dim - 1))

    # Ensure coordinates are within the bounds of the screen.
    return max(0, min(screen_coord, screen_dim - 1))

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

# Setup game play screen
def game_setup():
    global bg_color, fg_color, comp_color
    display.clear()
    bg_color = (random_color())
    fg_color = text_color(bg_color)
    comp_color = find_complementary_color(bg_color)
    display.fill(bg_color)

    # Generate a random dot on screen
    generate_random_dot()

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
    # Check if the game is started
    if start_game == 0:
        # Check if Button A is pressed to start the game for player 1
        if buttons.was_pressed(BTN_A):
            player = 1
            display.clear()
            clear_lights()
            leds.set(5, True)
            leds.set(4, False)
            start_game = 1
            # If player 1 hasn't played yet, set up the game
            if not p1_has_played:
                game_setup()

        # Check if Button B is pressed to start the game for player 2
        if buttons.was_pressed(BTN_B):
            player = 2
            display.clear()
            clear_lights()
            leds.set(4, True)
            leds.set(5, False)
            start_game = 1
            # If player 2 hasn't played yet, set up the game
            if not p2_has_played:
                game_setup()

    # Check if the game has started
    if start_game == 1:
        # Capture the accelerometer data
        xyz = accel.read()
        tilt_x, tilt_y, tilt_z = xyz

        # Ensure the game is still running
        if start_game != 0:
            # Display the player's score and remaining lives on the screen
            display.draw_text(f"Player {player} Score: {score}", x=5, y=230, color=fg_color, background=bg_color, scale=1)
            display.draw_text(f"Lives: {lives}", x=190, y=230, color=fg_color, background=bg_color, scale=1)

        # Scale accelerometer values to screen coordinates
        new_x = scale_accel_to_screen(tilt_x, -16576, 16576, SCREEN_WIDTH)
        new_y = scale_accel_to_screen(tilt_y, -16576, 16576, SCREEN_HEIGHT)
        
    # Check if Down Button is pressed to exit the game
    if buttons.was_pressed(BTN_D):
        break

# Call the exit program function to clean up and shut down the program
exit_program()