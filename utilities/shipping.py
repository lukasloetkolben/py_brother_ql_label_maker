import uuid
from pathlib import Path

import PIL.Image
from PIL.ImageQt import rgb
from pdf2image import convert_from_path

import config
from utilities.images import create_centered_image_on_background
from utilities.printer import get_label_by_identifier


def create_dhl_label(label, pdf_file_path: Path):
    label = get_label_by_identifier("102x152")
    height, width = label.dots_printable

    images = convert_from_path(pdf_file_path)
    if images:
        image = images[0]
        pdf_width, pdf_height = image.size

        w_2 = (pdf_width // 2)
        h_2 = (pdf_height // 2)
        # image.crop((left, top, right, bottom))
        image_1 = image.crop((65, 185, w_2 - 70, h_2 - 185))
        image_2 = image.crop((w_2 + 125, 185, pdf_width - 80, h_2 - 185))

        image_1_width, image_1_height = image_1.size
        image_2_width, image_2_height = image_2.size
        bg_width = image_1_width + image_2_width
        bg_height = max(image_2_height, image_1_height)
        background = PIL.Image.new("RGBA", (bg_width, bg_height), color=rgb(255, 255, 255))
        background.paste(image_1, (0, 0))
        background.paste(image_2, (image_1_width, 0))

        image = create_centered_image_on_background(background, width, height, bg_color=(255, 255, 255))
        output_path = Path(config.TEMP_DIR, f"{uuid.uuid1()}.png")
        image.save(str(output_path))

        return label, output_path

    return None, None


def create_hermes_label(label, pdf_file_path: Path):
    label = get_label_by_identifier("102x152")
    height, width = label.dots_printable

    images = convert_from_path(pdf_file_path)
    if images:
        image = images[0]
        pdf_width, pdf_height = image.size

        # image.crop((left, top, right, bottom))
        image = image.crop((77, 92, width - 207, (pdf_height // 2) - 123))
        image = create_centered_image_on_background(image, width, height, bg_color=(255, 255, 255))

        # Save the image
        output_path = Path(config.TEMP_DIR, f"{uuid.uuid1()}.png")
        image.save(str(output_path))
        return label, output_path

    return None, None


def create_ebay_stamp_label(label, pdf_file_path: Path):
    height, width = label.dots_printable

    images = convert_from_path(pdf_file_path)
    if images:
        image = images[0]
        pdf_width, pdf_height = image.size
        print(pdf_width, pdf_height)
        # image.crop((left, top, right, bottom))
        image = image.crop((120, 200, 725, 475))
        image = create_centered_image_on_background(image, width, height, bg_color=(255, 255, 255))

        # Save the image
        output_path = Path(config.TEMP_DIR, f"{uuid.uuid1()}.png")
        image.save(str(output_path))
        return label, output_path

    return None, None


shipping_companies = {
    'DHL': create_dhl_label,
    'Hermes': create_hermes_label,
    'eBay Stamp': create_ebay_stamp_label,
}
