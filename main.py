import io
import numpy as np
import pygame
import time
import os
import shutil

## Library Initialization
pygame.init()

## Image File Setup
IMAGE_MODE = 'SEARCH'
copy_to_directory = False

if IMAGE_MODE == 'SEARCH':
    # THis portion is based on an answer by Simimic on StackOverflow and an article on geeksforgeeks.org
    # https://stackoverflow.com/questions/66663179/
    # https://www.geeksforgeeks.org/python-askopenfile-function-in-tkinter/
    import tkinter
    from tkinter import filedialog
    tkinter.Tk().withdraw()                                             # Prevents an empty tkinter window from appearing
    IMAGE_PATH = filedialog.askopenfilename(filetypes=[('Image Files','*.png *.jpeg *.jpg')])
    IMAGE_NAME = os.path.basename(IMAGE_PATH)                           # Gets base file name
    directory_path = rf'/images/{IMAGE_NAME}'                           # Converts to main directory path
    if copy_to_directory == True and not os.path.isfile(directory_path):
        shutil.copy2(IMAGE_PATH, r'images')
        IMAGE_PATH = directory_path
elif IMAGE_MODE == 'DIRECTORY':
    # Insert Image Name Here
    IMAGE_PATH = r'images/good_luck_cappy.jpg'
else:
    IMAGE_PATH = r'images/good_luck_cappy.jpg'

## Window Position Setup
WINDOW_POSITION = (100, 100)
os.environ['SDL_VIDEO_WINDOW_POS'] = str(WINDOW_POSITION[0]) + "," + str(WINDOW_POSITION[1])

## Window Setup
window = pygame.display.set_mode((500, 500))
pygame.display.set_caption('Image to ASCII')

## Image Processing
SCALE_FACTOR = 0.2
pygame_image = pygame.image.load(IMAGE_PATH).convert()                  # Loads image into a new surface
pygame_image = pygame.transform.scale_by(pygame_image, SCALE_FACTOR)    # Scales the surface
#pygame_image_grayscale = pygame.transform.grayscale(pygame_image)      # Converts surface to grayscale

## Window Updating / Displaying Image
window = pygame.display.set_mode((pygame_image.get_size()))
window.blit(pygame_image, (0, 0))
pygame.display.flip()

## Character List
ASCII_PRINTABLE = '!\"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~'
ASCII_EXTENDED = 'ÇüéâäàåçêëèïîìÄÅÉæÆôöòûùÿÖÜø£Ø×ƒáíóúñÑªº¿®¬½¼¡«»░▒▓│┤ÁÂÀ©╣║╗╝¢¥┐└┴┬├─┼ãÃ╚╔╩╦╠═╬¤ðÐÊËÈıÍÎÏ┘┌█▄¦Ì▀ÓßÔÒõÕµþÞÚÛÙýÝ¯´≡±‗¾¶§÷¸°¨·¹³²■'
ASCII_FULL = ASCII_PRINTABLE + ASCII_EXTENDED

## Font Setup
FONT_PATH = r'/JetBrainsMono-2.304/fonts/ttf/JetBrainsMono-Regular.ttf'
FONT_SIZE = 100

# Counts distributions of colors
def get_surface_composition(gsc_surface):
    if not isinstance(gsc_surface, pygame.Surface):                     # Checks to see if parameter is the correct type
        raise TypeError

    gsc_surface_grayscale = pygame.transform.grayscale(gsc_surface)     # Converts surface to grayscale
    gsc_surface_list = []

    # Cycles through all grayscale colors
    for gsc_color in range(0, 256):
        gsc_pixels = pygame.transform.threshold(dest_surface=None,
                                                surface=gsc_surface_grayscale,
                                                search_color=(gsc_color, gsc_color, gsc_color),
                                                threshold=(0, 0, 0, 255),
                                                set_behavior=0)
        gsc_surface_list.append(gsc_pixels)
    gsc_surface_list = np.array(gsc_surface_list)
    return gsc_surface_list

# Creates a chart of input data
def make_chart(mc_data, mc_mode, mc_size):
    if not isinstance(mc_data, np.ndarray):
        raise TypeError
    
    mc_padding = 10

    mc_surface = pygame.Surface((len(mc_data) + (mc_padding * 2), np.max(mc_data) + (mc_padding * 2)))

    if mc_mode == 'line':
        for mc_x in range(0, len(mc_data) - 1):
            pygame.draw.line(mc_surface,
                               (255, 255, 255),
                               (mc_padding + mc_x, mc_surface.get_height() - (mc_padding + mc_data[mc_x])),
                               (mc_padding + mc_x + 1, mc_surface.get_height() - (mc_padding + mc_data[mc_x + 1])))

    mc_surface = pygame.transform.scale(mc_surface, mc_size)
    return mc_surface

window.blit(make_chart(get_surface_composition(pygame_image),'line', pygame_image.get_size()), (0, 0))

main_loop = True
while main_loop:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            main_loop = False

    pygame.display.flip()