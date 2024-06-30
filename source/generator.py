import argparse
from PIL import Image

# define constants
COMMENT_WIDTH = 25
COMMENT_HEIGHT = 13
FINAL_WIDTH = 2 * COMMENT_WIDTH
FINAL_HEIGHT = 4 * COMMENT_HEIGHT
PROPORTION = FINAL_WIDTH / FINAL_HEIGHT
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


def threshold(image: Image, theta: int) -> None:
    # get image dimansions
    width, height = image.size

    # get pixels
    pixels = image.load()

    for x in range(width):
        for y in range(height):
            # get rgb values from the current pixel,
            # use a try... except block to prevent failure
            # due to transparency
            try:
                r, g, b = pixels[x, y]
            except:
                r, g, b, _ = pixels[x, y]

            avg = (r + g + b) / 3

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


def create_ascii(image: Image) -> None:
    width, height = image.size


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
    image = crop(image)

    # resize the image
    image = resize(image)

    # perform the threshold to the image
    threshold(image, args.t)

    # save the image
    image.save(args.o)
