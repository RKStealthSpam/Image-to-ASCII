import io
import numpy as np
import pygame
import time
import os
import shutil

# Character List
ASCII_PRINTABLE = '!\"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~'
ASCII_EXTENDED = 'ÇüéâäàåçêëèïîìÄÅÉæÆôöòûùÿÖÜø£Ø×ƒáíóúñÑªº¿®¬½¼¡«»░▒▓│┤ÁÂÀ©╣║╗╝¢¥┐└┴┬├─┼ãÃ╚╔╩╦╠═╬¤ðÐÊËÈıÍÎÏ┘┌█▄¦Ì▀ÓßÔÒõÕµþÞÚÛÙýÝ¯´≡±‗¾¶§÷¸°¨·¹³²■'
print(ASCII_EXTENDED)

# Font Setup
FONT_PATH = r'/JetBrainsMono-2.304/fonts/ttf/JetBrainsMono-Regular.ttf'
FONT_SIZE = 100

# Window Position Setup
WINDOW_POSITION = (100, 100)
os.environ['SDL_VIDEO_WINDOW_POS'] = str(WINDOW_POSITION[0]) + "," + str(WINDOW_POSITION[1])

# Library Initialization
pygame.init()

# Window Setup
window = pygame.display.set_mode((500, 500))
pygame.display.set_caption('Image to ASCII')

# Image File Setup
IMAGE_MODE = 'SEARCH'
copy_to_directory = False

if IMAGE_MODE == 'SEARCH':
    # THis portion is based on an answer by Simimic on StackOverflow and an article on geeksforgeeks.org
    # https://stackoverflow.com/questions/66663179/
    # https://www.geeksforgeeks.org/python-askopenfile-function-in-tkinter/
    import tkinter
    from tkinter import filedialog
    tkinter.Tk().withdraw()  # prevents an empty tkinter window from appearing
    IMAGE_PATH = filedialog.askopenfilename(filetypes=[('Image Files','*.png *.jpeg *.jpg')])
    IMAGE_NAME = os.path.basename(IMAGE_PATH) # gets bases file name
    directory_path = rf'/images/{IMAGE_NAME}' #converts to main directory path

    if copy_to_directory == True and not os.path.isfile(directory_path):
        shutil.copy2(IMAGE_PATH, r'images')
        IMAGE_PATH = directory_path

elif IMAGE_MODE == 'DIRECTORY':
    # Insert Image Name Here
    IMAGE_PATH = r'/images/good_luck_cappy.jpg'
else:
    IMAGE_PATH = r'/images/good_luck_cappy.jpg'