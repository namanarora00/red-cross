from fpdf import FPDF
import code128
import os

import PIL.Image
import PIL.ImageTk

# Use Code-128 barcode type

def generate_barcode(ID: str):
    try:
        os.mkdir("bars")
    except FileExistsError:
        pass
    finally:
        # saves barcodes
        code128.image(ID).save(f"bars/{ID}.png")


def to_pdf():
    '''
        Takes images from bars directory and makes it to one PDF
    '''
    pdf = FPDF()

    try:
        images = os.listdir("bars")
    except FileNotFoundError:
        print(os.listdir("bars"))

    y = 0

    for i, image in enumerate(images):
        if(i%6==0):
            pdf.add_page()
            y = 0
        pdf.image(os.path.join("bars", image), y=y)
        y += 50
    pdf.output("barcodes.pdf", "F")


if __name__ == "__main__":
    generate_barcode("100")

