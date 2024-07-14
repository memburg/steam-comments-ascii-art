import os
import argparse
from PIL import Image

# define constants
COMMENT_WIDTH = 25
COMMENT_HEIGHT = 13
FINAL_WIDTH = 2 * COMMENT_WIDTH
FINAL_HEIGHT = 4 * COMMENT_HEIGHT
PROPORTION = FINAL_WIDTH / FINAL_HEIGHT
BRAILLE_SIZE = 192
BRAILLE_CHARACTERS = "".join(
    [
        "⡀⡁⡂⡃⡄⡅⡆⡇⡈⡉⡊⡋⡌⡍⡎⡏",
        "⡐⡑⡒⡓⡔⡕⡖⡗⡘⡙⡚⡛⡜⡝⡞⡟",
        "⡠⡡⡢⡣⡤⡥⡦⡧⡨⡩⡪⡫⡬⡭⡮⡯",
        "⡰⡱⡲⡳⡴⡵⡶⡷⡸⡹⡺⡻⡼⡽⡾⡿",
        "⢀⢁⢂⢃⢄⢅⢆⢇⢈⢉⢊⢋⢌⢍⢎⢏",
        "⢐⢑⢒⢓⢔⢕⢖⢗⢘⢙⢚⢛⢜⢝⢞⢟",
        "⢠⢡⢢⢣⢤⢥⢦⢧⢨⢩⢪⢫⢬⢭⢮⢯",
        "⢰⢱⢲⢳⢴⢵⢶⢷⢸⢹⢺⢻⢼⢽⢾⢿",
        "⣀⣁⣂⣃⣄⣅⣆⣇⣈⣉⣊⣋⣌⣍⣎⣏",
        "⣐⣑⣒⣓⣔⣕⣖⣗⣘⣙⣚⣛⣜⣝⣞⣟",
        "⣠⣡⣢⣣⣤⣥⣦⣧⣨⣩⣪⣫⣬⣭⣮⣯",
        "⣰⣱⣲⣳⣴⣵⣶⣷⣸⣹⣺⣻⣼⣽⣾⣿",
    ]
)
BRAILLE_IMAGES = os.listdir("braille")  # create logic to ignore this file '.DS_Store'


def threshold(image: Image, theta: int) -> None:
    # get image dimansions
    width, height = image.size

    # get pixels
    pixels = image.load()

    for x in range(width):
        for y in range(height):
            r, g, b = pixels[x, y]

            avg = (r + g + b) // 3

            if avg < theta:
                # set the pixel to black
                pixels[x, y] = (0, 0, 0)
            else:
                # set the pixel to white
                pixels[x, y] = (255, 255, 255)


def resize(image: Image) -> Image:
    return image.resize((FINAL_WIDTH, FINAL_HEIGHT))


def crop(image: Image) -> None:
    """
    height = 52
    width = 50

    relation = 0.961538461538
    """
    # get image dimansions
    width, height = image.size
    new_width = height * PROPORTION
    to_centre = (width - new_width) // 2

    return image.crop((to_centre, 0, new_width + to_centre, height))


def extract_subimage(image: Image, x: int, y: int) -> Image:
    print(f"{x} -> {x + 1}, {y} -> {y + 3}")
    return image.crop((x, y, x + 2, y + 4))


def get_ascii_character(image: Image) -> str:
    # get pixels from the subimage (2x4)
    subimage_pixels = image.load()

    for ascii_image in BRAILLE_IMAGES:
        if ".DS_Store" == ascii_image:
            continue

        braille = Image.open(f"braille/{ascii_image}")
        braille = braille.convert("1")
        braille_pixels = braille.load()
        matches = 0

        for x in range(2):
            for y in range(4):
                p1 = braille_pixels[x, y]
                p2 = subimage_pixels[x, y]

                if p1 == p2:
                    matches += 1

        if matches == 8:
            print("match found")
            return BRAILLE_CHARACTERS[int(ascii_image[8:11])]

    return " "


def get_ascii_image(image: Image) -> str:
    width, height = image.size
    ascii_image = []

    for y in range(0, height, 4):
        ascii_row = []
        for x in range(0, width, 2):
            subimage = extract_subimage(image, x, y)
            ascii_row.append(get_ascii_character(subimage))

        ascii_image.append(ascii_row)

    return ascii_image


if __name__ == "__main__":
    # create the parser object
    parser = argparse.ArgumentParser(
        description="Arguments parser for our ascii art generator"
    )

    # create optional arguments
    parser.add_argument("--t", type=int, default=100, help="Thresholding range")
    parser.add_argument("--o", type=str, default="ascii.png", help="Output name")

    # create required arguments
    parser.add_argument("image_path", type=str, help="Path to the input image")

    # parse arguments
    args = parser.parse_args()

    # load the image
    image = Image.open(args.image_path)
    image = image.convert("RGB")
    image = crop(image)

    # resize the image
    image = resize(image)

    # perform the threshold to the image
    threshold(image, args.t)

    # convert the image to a binary image
    image = image.convert("1")

    # save the image
    image.save(args.o)

    print(get_ascii_image(image))
