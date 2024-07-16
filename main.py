from codex import *

# Initialize global variables
bg_color = (0, 0, 0)

# Generate a randomly generated RGB color
def random_color():
    red = random.randrange(0, 256)
    green = random.randrange(0, 256)
    blue = random.randrange(0, 256)
    return red, green, blue # returns a tuple in (r, g, b) format