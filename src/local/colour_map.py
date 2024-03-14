import os
import numpy as np
import colorsys
from collections import Counter
from PIL import Image

def get_most_common_color(image_path):
    image = Image.open(image_path)
    if image.mode != 'RGBA':
        image = image.convert('RGBA')
    pixels = np.array(image)
    pixels = pixels.reshape(-1, 4)
    pixels = pixels[pixels[:, 3] > 0][:, :3]
    colors = Counter(map(tuple, pixels))
    non_black_threshold = 50
    colors = {color: count for color, count in colors.items() if all(value > non_black_threshold for value in color)}
    most_common_non_black_color = max(colors, key=colors.get) if colors else (255, 255, 255)
    return tuple(map(int, most_common_non_black_color))

def get_complementary_color(rgb):
    r, g, b = [x / 255.0 for x in rgb]
    h, s, v = colorsys.rgb_to_hsv(r, g, b)
    h = (h + 0.5) % 1.0
    r, g, b = colorsys.hsv_to_rgb(h, s, v)
    return tuple(int(x * 255) for x in (r, g, b))

def process_images_in_directory(directory_path):
    image_colors_map = {}
    for file_name in os.listdir(directory_path):
        if not file_name.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            continue  # Skip non-image files
        image_path = os.path.join(directory_path, file_name)
        most_common_color = get_most_common_color(image_path)
        complementary_color = get_complementary_color(most_common_color)
        image_colors_map[image_path] = (most_common_color, complementary_color)
    return image_colors_map

directory_path = 'media/AccelitherHeads'
result = process_images_in_directory(directory_path)
print(result)

