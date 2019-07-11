import barcode
from barcode.writer import ImageWriter
import os

# Use Code-128 barcode type

C128 = barcode.get_barcode_class('code128')


def generate_barcode(ID: str):
    try:
        os.mkdir("bars")
    except FileExistsError:
        pass

    b = C128(ID, writer=ImageWriter())
    b.save("bars/" + ID)


if __name__ == "__main__":
    generate_barcode("100")
