#!/usr/bin/python3

import argparse
import imghdr
import random
from os import system
from PIL import Image
from pathlib import Path

PIXEL_CHAR = '██'

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
    for f in Path(img_path).iterdir():
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

for y in range(height):
    ansi_str = ''
    for x in range(width):
        red, green, blue, alpha = img.getpixel((x, y))
        if alpha == 255:
            ansi_str += f'\x1b[38;2;{red};{green};{blue}m{PIXEL_CHAR}\x1b[0m'
        else:
            ansi_str += '  '
    ansi_str += '\n'
    system(f'printf "{ansi_str}"')

print()
