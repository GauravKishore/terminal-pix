#!/usr/bin/python3

import argparse
import imghdr
import numpy as np
import random
from os import system
from PIL import Image, UnidentifiedImageError
from pathlib import Path

PIXEL_CHAR = '██'

parser = argparse.ArgumentParser()

parser.add_argument('img_path',
                    metavar='img-path',
                    type=Path,
                    help="path to an image file or a directory containing image files to randomly select image from")

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
img = np.asarray(img)

for i in range(img.shape[0]):
    ansi_str = ''
    for j in range(img.shape[1]):
        pixel = img[i, j, :]
        red = pixel[0]
        green = pixel[1]
        blue = pixel[2]
        alpha = pixel[3]
        if alpha:
            ansi_str += f'\x1b[38;2;{red};{green};{blue}m{PIXEL_CHAR}\x1b[0m'
        else:
            ansi_str += '  '
    ansi_str += '\n'
    system(f'printf "{ansi_str}"')

print()
