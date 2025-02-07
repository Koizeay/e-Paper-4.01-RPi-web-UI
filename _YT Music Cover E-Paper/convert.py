from PIL import Image, ImageOps
import numpy as np


def closest_color(pixel, palette):
    pixel = np.array(pixel, dtype=np.int32)
    palette = np.array(palette, dtype=np.int32)
    distances = np.linalg.norm(palette - pixel, axis=1)
    return tuple(palette[np.argmin(distances)])


def process_image(input_path, output_path):
    color_palette = [
        (0, 0, 0),  # Black (#000000)
        (255, 255, 255),  # White (#FFFFFF)
        (0, 255, 0),  # Green (#00FF00)
        (0, 0, 255),  # Blue (#0000FF)
        (255, 0, 0),  # Red (#FF0000)
        (255, 255, 0),  # Yellow (#FFFF00)
    ]

    image = Image.open(input_path)
    min_dim = min(image.size)
    left = (image.width - min_dim) // 2
    top = (image.height - min_dim) // 2
    right = left + min_dim
    bottom = top + min_dim
    image = image.crop((left, top, right, bottom))

    image = ImageOps.contain(image, (640, 400), Image.LANCZOS)
    new_image = Image.new("RGB", (640, 400), (255, 255, 255))
    new_image.paste(image, ((640 - image.width) // 2, (400 - image.height) // 2))

    new_image = new_image.convert('RGB')

    pixels = np.array(new_image)

    for y in range(pixels.shape[0]):
        for x in range(pixels.shape[1]):
            pixels[y, x] = closest_color(pixels[y, x], color_palette)

    final_image = Image.fromarray(np.uint8(pixels))

    final_image.save(output_path, format='BMP')


if __name__ == "__main__":
    process_image("./temp/source.jpg", "./temp/output.bmp")
