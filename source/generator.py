import argparse
from PIL import Image


def get_pixels(image_path: str):
    # Open an image file
    image = Image.open(image_path)

    # Get the image dimensions
    width, height = image.size

    # Load image data
    pixels = image.load()

    print(width, height)


if __name__ == "__main__":
    # create the parser object
    parser = argparse.ArgumentParser(
        description="Arguments parser for our ascii art generator"
    )

    # create optional arguments
    parser.add_argument("--c", type=str, default="centre", help="Crop mode")
    parser.add_argument("--o", type=str, default="output.txt", help="Output name")
    parser.add_argument("--t", type=str, default="output.txt", help="Thresholding mode")

    # create required arguments
    parser.add_argument("image_path", type=str, help="Path to the input image")

    # parse arguments
    args = parser.parse_args()

    # start the image processing
    get_pixels(args.image_path)
