import pygame

# Initialize Pygame
pygame.init()

# Create a surface
surface = pygame.Surface((800, 600))

# Fill the surface with black color
surface.fill((0, 0, 0))

# Get the pixel array of the surface
pixels = pygame.PixelArray(surface)

# Iterate over each pixel
for x in range(surface.get_width()):
    for y in range(surface.get_height()):
        # Check if the pixel is black
        if pixels[x, y] == (0, 0, 0):
            # Replace black pixel with white pixel
            pixels[x, y] = (255, 255, 255)

# Delete the pixel array to update the surface
del pixels

# Quit Pygame
pygame.quit()