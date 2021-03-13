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

parser.add_argument('img_dir',
                    metavar='img-dir',
                    type=Path,
                    help="directory to randomly select image from")

args = parser.parse_args()
img_dir = args.img_dir

if not img_dir.is_dir():
    raise NotADirectoryError(f"No directory: {img_dir}")

img_paths = []
for f in Path(img_dir).iterdir():
    if f.is_file() and imghdr.what(f):
        img_paths.append(f)

img = Image.open(random.choice(img_paths))
img = img.convert('RGBA')
img = np.asarray(img)

ansi_str = ''
for i in range(img.shape[0]):
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

ansi_str += '\n'

system(f'printf "{ansi_str}"')
