import argparse
from PIL import Image

# define constants
COMMENT_WIDTH = 13
COMMENT_HEIGHT = 25
FINAL_WIDTH = 2 * COMMENT_WIDTH
FINAL_HEIGHT = 4 * COMMENT_HEIGHT
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
            # get rgb values from the current pixel
            r, g, b = pixels[x, y]
            avg = (r + g + b) / 3

            if avg < theta:
                # set the pixel to black
                pixels[x, y] = (0, 0, 0)
            else:
                # set the pixel to white
                pixels[x, y] = (255, 255, 255)


def crop(image: Image) -> None:
    # width = 26 13
    # height = 100 50
    pass


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

    # perform the threshold to the image
    threshold(image, args.t)
    crop(image)

    # save the image
    image.save(args.o)
