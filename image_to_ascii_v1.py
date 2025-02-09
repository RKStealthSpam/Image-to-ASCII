import numpy as np
import pygame
import time
import os

position = (100, 100)
os.environ['SDL_VIDEO_WINDOW_POS'] = str(position[0]) + "," + str(position[1])
pygame.init()

# List appears in ASCII order
characters = ' !\"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~'

# Font Settings
# Width of text should be 0.6 * FONT_SIZE * length of string
# Height of text should be 1.321 * FONT_SIZE
FONT_SIZE = 100
FONT = 'Jetbrains Mono'

# Program Display Setup
window = pygame.display.set_mode((500, 500))
pygame.display.set_caption('ASCII Image Converter')

# Image File Path(s)
image_path = r'C:\Users\huevo\OneDrive\Pictures\Heavy Portrait.jpg'     # Heavy portrait
#image_path = r'C:\Users\huevo\OneDrive\Pictures\aperture logo.png'     # CRT-style Aperture logo

# Image Processing
image = pygame.image.load(image_path).convert()                         # Loads image into a new Surface
image = pygame.transform.grayscale(image)                               # Converts image into greyscale
#image = pygame.transform.scale_by(image, 0.5)                          # Scales the image

# Window Updating / Displaying Image
window = pygame.display.set_mode((image.get_size()))
window.blit(image, (0, 0))


#for row in range(0, int(window.get_height() / (FONT_SIZE * 1.321)) + 1):
#    font = pygame.font.SysFont(FONT, FONT_SIZE)
#    text_surface = font.render(characters, False, (255, 255, 255), (0, 0, 0))
#    window.blit(text_surface, (0, row * int(FONT_SIZE * 1.321)))

#pygame.display.flip()


# Generates and processes separate Surfaces for each included character
def generate_character_surfaces(gcs_font, gcs_font_size, gcs_characters):
    gcs_font_object = pygame.font.SysFont(gcs_font, gcs_font_size)                  # Creates Font object
    gcs_black_surface = pygame.surface.Surface((round(gcs_font_size * 0.6, 0),      # Creates black Surface
                                                round(gcs_font_size * 1.321, 0)))

    gcs_list = []                                                                   # Empty list to sort into

    # Character processing loop
    for gcs_character in range(len(gcs_characters)):
        # Create a Surface containing the character
        gcs_character_surface = gcs_font_object.render(gcs_characters[gcs_character],
                                                       False,
                                                       (255, 255, 255))

        # Reset black Surface
        gcs_black_surface.fill((0, 0, 0))

        # Load character into the black Surface
        gcs_black_surface.blit(gcs_character_surface, (0, 0))

        # Find the potential color change of the character
        gcs_average_change = sum(pygame.transform.average_color(gcs_black_surface)[0:1]) / 255

        # Package data
        gcs_list.append([gcs_characters[gcs_character], gcs_character_surface, gcs_average_change])

    return gcs_list


def calculate_best_character(cbc_surface, cbc_character_data):
    # Calculates best character for a given subsurface
    cbc_surface_average = sum(pygame.transform.average_color(cbc_surface)[0:3]) / 3 / 255
    cbc_weights = []
    cbc_min_weight = ['', 5]

    for cbc_character in range(0, len(cbc_character_data)):
        cbc_work_surface = pygame.surface.Surface(cbc_surface.get_size())
        cbc_work_surface.blit(cbc_surface, (0, 0))

        cbc_work_surface.blit(cbc_character_data[cbc_character][1], (0, 0))

        #cbc_character_data[cbc_character].append((sum(pygame.transform.average_color(cbc_work_surface)[0:3]) / 3 / 255) - cbc_surface_average)
        #cbc_weights.append(cbc_character_data[cbc_character][2] * cbc_character_data[cbc_character][3])

        cbc_weights.append((sum(pygame.transform.average_color(cbc_work_surface)[0:3]) / 3 / 255) - cbc_surface_average)
        #print(cbc_weights[cbc_character])
        #print(cbc_character_data[cbc_character][0] + str(cbc_weights[cbc_character]))

        cbc_min_weight[0] = cbc_character_data[cbc_character][0]
        if cbc_min_weight[1] > cbc_weights[cbc_character] > 0.0:
            cbc_min_weight[1] = cbc_weights[cbc_character]

    cbc_true_min = min(cbc_weights[1::])
    #print(cbc_character_data[cbc_weights.index(cbc_true_min)][0])
    return cbc_min_weight[0]


def find_image_colors(fic_image):
    fic_image = pygame.transform.grayscale(fic_image)

    for fic_color in range(0, 256):
        fic_pixels = pygame.transform.threshold(dest_surface=None,
                                                surface=fic_image,
                                                search_color=(fic_color, fic_color, fic_color),
                                                threshold=(0, 0, 0, 255),
                                                set_behavior=0)
        print(fic_pixels)
        if fic_pixels >= (fic_image.get_width() * fic_image.get_height()) * 0:
            print(fic_color)
            fic_pixels = pygame.transform.threshold(dest_surface=window,
                                                    surface=fic_image,
                                                    search_color=(fic_color, fic_color, fic_color),
                                                    threshold=(0, 0, 0, 255),
                                                    set_color=(fic_color, 255 - fic_color, 255 - fic_color, 255),
                                                    set_behavior=1,
                                                    inverse_set=True)
            pygame.display.flip()


find_image_colors(image)
print(pygame.transform.average_color(image))


def generate_ascii_representation(gar_image, gar_font, gar_font_size, gar_characters):
    #gar_image = pygame.transform.grayscale(gar_image)
    gar_character_data = generate_character_surfaces(gar_font, gar_font_size, gar_characters)
    gar_ascii_list = []

    for gar_row in range(0, int(gar_image.get_height() / (gar_font_size * 1.321))):
        gar_ascii_list.append('')
        #check coords
        for gar_column in range(0, int(gar_image.get_width() / (gar_font_size * 0.6))):
            gar_image_subsurface = gar_image.subsurface((round(gar_column * (gar_font_size * 0.6), 0),
                                                         round((gar_row * gar_font_size * 1.321), 0),
                                                         round(gar_font_size * 0.6, 0),
                                                         round(gar_font_size * 1.321, 0)))
            gar_image_slice = pygame.surface.Surface(gar_image_subsurface.get_size())
            gar_image_slice.blit(gar_image_subsurface, (0, 0))
            gar_ascii_list[gar_row] = gar_ascii_list[gar_row] + (calculate_best_character(gar_image_slice, gar_character_data))
            #print(str(round(gar_column * (gar_font_size * 0.6), 0) + round(gar_font_size * 0.6, 0)) + ' '+ str(round((gar_row * gar_font_size * 1.321), 0) + round(gar_font_size * 1.321, 0)))
            #print(int(gar_image.get_width() / (gar_font_size * 0.6)))

    return gar_ascii_list


#test_character_list = generate_character_surfaces(FONT, FONT_SIZE, characters)
#for character in range(len(test_character_list)):
    #print(test_character_list[character])

#est_subsurface = window.subsurface((0, 0, 14, 32))
#test_surface = pygame.surface.Surface(test_subsurface.get_size())
#test_surface.blit(test_subsurface, (0, 0))
#calculate_best_character(test_surface, generate_character_surfaces(FONT, FONT_SIZE, characters))

test_ascii_list = generate_ascii_representation(image, FONT, FONT_SIZE, characters)
font = pygame.font.SysFont(FONT, FONT_SIZE)
#for row in range(0, len(test_ascii_list)):
#    text_surface = font.render(test_ascii_list[row], False, (255, 255, 255), (0, 0, 0))
#    window.blit(text_surface, (0, row * FONT_SIZE * 1.321))

pygame.display.flip()




run_loop = True

while run_loop:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run_loop = False

    #for row in range(0, int(window.get_height() / (FONT_SIZE * 1.321)) + 1):
    #    font = pygame.font.SysFont(FONT, FONT_SIZE)
    #    text_surface = font.render(characters, False, (255, 255, 255), (0, 0, 0))
    #   window.blit(text_surface, (0, row * int(FONT_SIZE * 1.321)))

    #for character in range(0, len(test_character_list)):
    #    window.blit(test_character_list[character][1], (0, 0))
    #    pygame.display.flip()
    #    time.sleep(0)
    pygame.display.flip()
    time.sleep(0.1)
    #run_loop = False


