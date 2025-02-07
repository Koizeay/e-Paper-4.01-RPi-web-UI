from PIL import Image
import numpy as np

def closest_color(pixel, palette):
    pixel = np.array(pixel, dtype=np.int32)
    palette = np.array(palette, dtype=np.int32)
    distances = np.linalg.norm(palette - pixel, axis=1)
    return tuple(palette[np.argmin(distances)])

def process_image(input_path, output_path):
    color_palette = [
        (0, 0, 0),       # Black (#000000)
        (255, 255, 255), # Whie (#FFFFFF)
        (0, 255, 0),     # Green (#00FF00)
        (0, 0, 255),     # Blue (#0000FF)
        (255, 0, 0),     # Red (#FF0000)
        (255, 255, 0),   # Yellow (#FFFF00)
        #(255, 170, 0)    # Orange (#FFAA00), not working well
    ]

    image = Image.open(input_path)
    image = image.resize((640, 400), Image.LANCZOS)
    image = image.convert('RGB')
    pixels = np.array(image)
    
    for y in range(pixels.shape[0]):
        for x in range(pixels.shape[1]):
            pixels[y, x] = closest_color(pixels[y, x], color_palette)

    new_image = Image.fromarray(np.uint8(pixels))
    new_image.save(output_path, format='BMP')
    
if __name__ == "__main__":
    process_image("./source.png", "./output.bmp")
