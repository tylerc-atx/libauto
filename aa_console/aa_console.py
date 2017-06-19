#!/usr/bin/env python3

import pygame, sys
from collections import deque
import os
import io

DIR_PATH = os.path.dirname(os.path.realpath(__file__))


# Settings:
CONSOLE_FONT_SIZE = 30
HEADER_FONT_SIZE = 45
BG_COLOR = (0, 0, 0)
HEADER_BG_COLOR = (136, 204, 136)
HEADER_TXT_COLOR = (0, 68, 0)
CONSOLE_BG_COLOR = (255, 255, 255)
CONSOLE_TXT_COLOR = (0, 0, 255)
CONSOLE_TXT_BG_COLOR = (198, 205, 246)
HEADER_CONSOLE_SPLIT = 7
HEADER_TITLE = 'AutoAuto Console'
HEADER_FONT_PATH = os.path.join(DIR_PATH, '../resources/fonts/DejaVuSansMono-Bold.ttf')
CONSOLE_FONT_PATH = os.path.join(DIR_PATH, '../resources/fonts/DejaVuSansMono.ttf')
LOGO_PATH = os.path.join(DIR_PATH, '../resources/images/logo_2017_03_17.png')

# Init pygame:
pygame.init()

# Create the window.
window_surface = pygame.display.set_mode()
window_width, window_height = window_surface.get_size()
pygame.display.set_caption(HEADER_TITLE)
pygame.mouse.set_visible(False)
window_surface.fill(BG_COLOR, window_surface.get_rect())

# Define the window areas:
full_rect = pygame.Rect(20, 20, window_width-40, window_height-40)
header_rect = pygame.Rect(full_rect.x, full_rect.y, full_rect.width, full_rect.height//HEADER_CONSOLE_SPLIT)
console_rect = pygame.Rect(full_rect.x, header_rect.y + header_rect.height, full_rect.width, full_rect.height-header_rect.height)

# The fonts we'll use:
console_font = pygame.font.Font(CONSOLE_FONT_PATH, CONSOLE_FONT_SIZE)
header_font = pygame.font.Font(HEADER_FONT_PATH, HEADER_FONT_SIZE)

# Draw the header:
window_surface.fill(HEADER_BG_COLOR, header_rect)
logo = pygame.image.load(LOGO_PATH)
logo_width, logo_height = logo.get_rect().size
image_size = (header_rect.height * logo_width // logo_height, header_rect.height)
logo = pygame.transform.scale(logo, image_size)
image_rect = pygame.Rect(console_rect.x + console_rect.width - image_size[0], header_rect.y, *image_size)
window_surface.blit(logo, image_rect)
title_text = header_font.render(HEADER_TITLE, True, HEADER_TXT_COLOR)
window_surface.blit(title_text, (header_rect.x + 10, header_rect.y + 10))

# Draw the console:

def parse_text(new_text, old_lines, outer_rect):

    for char in new_text:

        if char == '\r':
            continue

        sprite = console_font.render(char, True, CONSOLE_TXT_COLOR, CONSOLE_TXT_BG_COLOR)
        rect = sprite.get_rect()

        last_line = old_lines[-1]

        if char == '\n':
            last_line.append((char, sprite))
            old_lines.append([])

        else:
            if len(last_line) < (outer_rect.width // rect.width):
                last_line.append((char,sprite))
            else:
                old_lines.append([(char, sprite)])

        while len(old_lines) > (outer_rect.height // rect.height):
            old_lines.popleft()


def draw_lines(lines, outer_rect):
    x, y = outer_rect.topleft
    for line in lines:
        for char, sprite in line:
            rect = sprite.get_rect()
            rect.topleft = (x, y)
            if char != '\n':
                window_surface.blit(sprite, rect)
            x += rect.width
        if line:
            x = outer_rect.x
            y += line[0][1].get_rect().height


lines = deque()
lines.append([])


"""
See: https://docs.python.org/3.1/library/sys.html#sys.stdin
"""
inbuf = sys.stdin.detach()


def my_read(num_bytes):
    if num_bytes <= 0:
        return b''
    b = inbuf.read(num_bytes)
    if len(b) != num_bytes:
        sys.exit()
    return b


stream_img = None


while True:
    window_surface.fill(CONSOLE_BG_COLOR, console_rect)
    draw_lines(lines, console_rect)
    if stream_img is not None:
        window_surface.blit(stream_img, console_rect)
    pygame.display.update()

    chunk_type = int.from_bytes(my_read(1), byteorder='big')
    chunk_len  = int.from_bytes(my_read(4), byteorder='big')
    chunk      = my_read(chunk_len)

    if chunk_type == 0:
        # Clear the text on the screen.
        lines = deque()
        lines.append([])

    if chunk_type == 0 or chunk_type == 1:
        # Text to display.
        text = chunk.decode('utf-8')
        parse_text(text, lines, console_rect)

    if chunk_type == 2:
        # Image to display.
        chunk_buf = io.BytesIO(chunk)
        stream_img = pygame.image.load(chunk_buf)

    if chunk_type == 3:
        # Clear the image.
        stream_img = None

