import traceback
import uuid
from pathlib import Path

import PIL.Image

from PIL import ImageOps
import PIL.Image
from PIL import ImageDraw, ImageFont
from PIL import ImageOps

import config


def create_centered_image_on_background(image, width, height, bg_color=(255, 255, 255)):
    """
    Create a new image with a centered image pasted onto a blank background.
    Returns:
        PIL.Image: The new image with the input image centered on a blank background.
    """
    width = int(width)
    height = int(height)
    image = ImageOps.contain(image, (width, height))

    background = PIL.Image.new("RGBA", (width, height), color=bg_color)

    image_width, image_height = image.size

    x_offset = (width - image_width) // 2
    y_offset = (height - image_height) // 2
    try:
        background.paste(image, (x_offset, y_offset), image)
    except Exception:
        background.paste(image, (x_offset, y_offset))

    return background


def create_icon_text_image(width, height, text="", font_size=45, font_family="Arial", icon_path = None, icon_size=.8):
    """
    Create a labeled image with the input text added to the selected image and save it.
    """
    text = text.strip()

    if icon_path is not None and Path(icon_path).is_file():
        icon = PIL.Image.open(icon_path)
        # Scale the image to the desired height while maintaining the aspect ratio
        icon_height = int(height * icon_size)
        icon_width = int(icon_height * icon.width / icon.height)
        icon = icon.resize((icon_width, icon_height), PIL.Image.LANCZOS)
    else:
        icon_height = 1
        icon_width = 1
        icon = PIL.Image.new("RGBA", (icon_height, icon_width), color=(255, 255, 255, 0))

    # Create a blank white background image of the desired size
    background = PIL.Image.new("RGBA", (width, height), color=(255, 255, 255, 255))

    # Paste the scaled image on the top-left of the background image
    x_offset = 10
    y_offset = (height - icon_height) // 2
    try:
        background.paste(icon, (x_offset, y_offset), icon)
    except Exception:
        traceback.print_exc()
        background.paste(icon, (x_offset, y_offset))

    # Create an ImageDraw object to draw on the background image
    draw = ImageDraw.Draw(background)

    # Get the dimensions of the text using the provided font_size
    font = ImageFont.truetype(f"{font_family}.ttf", font_size)
    text_width, text_height = font.getsize(text)

    # Calculate the available width for the text
    available_width = width - icon_width - x_offset

    # Reduce the font size until the text fits within the available width
    while text_width > (available_width - 60):
        text_size -= 5
        font = ImageFont.truetype(font_family, text_size)
        text_width, text_height = font.getsize(text)

    # Calculate the text_x coordinate to center the text between the icon and the right edge
    text_x = icon_width + (available_width - text_width) // 2
    text_y = (height // 2) - (text_height // 2)

    # Draw the text on the image
    draw.text((text_x, text_y), text, fill="black", font=font)

    # Save the image
    output_path = Path(config.TEMP_DIR, f"{uuid.uuid1()}.png")
    background = background.rotate(90, expand=True)
    background.save(str(output_path))

    return output_path
