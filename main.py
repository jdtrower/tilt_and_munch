from codex import *

# Initialize global variables
bg_color = (0, 0, 0)
fg_color = (255, 255, 255)

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