#!/usr/bin/env python3

import pygame, sys
from collections import deque
import os

DIR_PATH = os.path.dirname(os.path.realpath(__file__))


# Settings:
CONSOLE_FONT_SIZE = 32
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


while True:
    window_surface.fill(CONSOLE_BG_COLOR, console_rect)
    draw_lines(lines, console_rect)
    pygame.display.update()

    # This is unfortunate. If we ask python for, say, 100 characters it will wait for
    # exactly 100 or until EOF. What would be better would be to return the number of
    # characters which are available immediately on the stream, but alas, it doesn't.
    # (That's what the system-call `read()` does, but python doesn't follow that patter.)
    # So, as a workaround, we'll just ask for one character at-a-time here:
    text = sys.stdin.read(1)
    if text == '':
        sys.exit()
    parse_text(text, lines, console_rect)

