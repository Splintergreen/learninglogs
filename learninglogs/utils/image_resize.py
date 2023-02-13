from django.core.files import File
from pathlib import Path
from PIL import Image
import datetime
from io import BytesIO

offset = datetime.timedelta(hours=3)
tz = datetime.timezone(offset, name='МСК')
image_types = {
    "jpg": "JPEG",
    "jpeg": "JPEG",
    "png": "PNG",
    "gif": "GIF",
    "tif": "TIFF",
    "tiff": "TIFF",
}


def image_resize(image, username, width, height):
    img = Image.open(image)
    image_name = f'{username}_{datetime.datetime.now(tz=tz)}'
    if img.width > width or img.height > height:
        output_size = (width, height)
        img.thumbnail(output_size)
        img_suffix = Path(image.file.name).name.split(".")[-1]
        img_filename = f'{image_name}.{img_suffix}'
        img_format = image_types[img_suffix]
        buffer = BytesIO()
        img.save(buffer, format=img_format)
        file_object = File(buffer)
        image.save(img_filename, file_object)
