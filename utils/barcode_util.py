from fpdf import FPDF
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


def to_pdf():
    '''
        Takes images from bars directory and makes it to one PDF
    '''
    pdf = FPDF()

    try:
        images = os.listdir("bars")
    except FileNotFoundError:
        print(os.listdir("bars"))

    for i, image in enumerate(images):
        if i % 2 == 0:
            pdf.add_page()
        pdf.image(os.path.join("bars", image), )
    pdf.output("barcodes.pdf", "F")


if __name__ == "__main__":
    generate_barcode("100")
