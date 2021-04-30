#!/usr/bin/python3

import argparse
import imghdr
import random
from os import system
from PIL import Image
from pathlib import Path

UPPER_BLOCK = '▀'
LOWER_BLOCK = '▄'
EMPTY = ' '
parser = argparse.ArgumentParser()

parser.add_argument('img_path',
                    metavar='img-path',
                    type=Path,
                    help="path to an image file or a directory containing image files to randomly "
                         "select an image from")

args = parser.parse_args()
img_path = args.img_path

if img_path.is_dir():
    img_paths = []
    for f in Path(img_path).rglob('*'):
        if f.is_file() and imghdr.what(f):
            img_paths.append(f)

    if not img_paths:
        raise FileNotFoundError(f"No image files found in directory: {img_path}")

    img = Image.open(random.choice(img_paths))
elif img_path.is_file():
    if not imghdr.what(img_path):
        raise TypeError(f"File is not a supported image file type: {img_path}")

    img = Image.open(img_path)
else:
    raise FileNotFoundError(f"No file or directory: {img_path}")

img = img.convert('RGBA')
width, height = img.size

print()

for y in range(0, height, 2):
    ansi_str = ' '
    for x in range(width):
        red_upper, green_upper, blue_upper, alpha_upper = img.getpixel((x, y))
        if (y + 1 < height):
            red_lower, green_lower, blue_lower, alpha_lower = img.getpixel((x, y + 1))
        else:
            red_lower, green_lower, blue_lower, alpha_lower = 0, 0, 0, 0

        if alpha_upper == 255 and alpha_lower == 255:
            pixel_char = UPPER_BLOCK
            ansi_fg = f'{red_upper};{green_upper};{blue_upper}'
            ansi_bg = f'{red_lower};{green_lower};{blue_lower}'
            ansi_str += f'\x1b[38;2;{ansi_fg};48;2;{ansi_bg}m{pixel_char}\x1b[0m'
        elif alpha_upper == 255:
            pixel_char = UPPER_BLOCK
            ansi_fg = f'{red_upper};{green_upper};{blue_upper}'
            ansi_str += f'\x1b[38;2;{ansi_fg}m{pixel_char}\x1b[0m'
        elif alpha_lower == 255:
            pixel_char = LOWER_BLOCK
            ansi_bg = f'{red_lower};{green_lower};{blue_lower}'
            ansi_str += f'\x1b[38;2;{ansi_bg}m{pixel_char}\x1b[0m'
        else:
            ansi_str += ' '

    ansi_str += '\n'
    system(f'printf "{ansi_str}"')

print()
