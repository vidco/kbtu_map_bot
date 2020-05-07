from io import BytesIO

from PIL import Image
from PIL.ImageDraw2 import Pen, Draw


def draw(delimited_path):

    pen = Pen(color="red", width=3)
    bytes_list = []

    for floor, paths in delimited_path.items():
        image = Image.open(f'images/{floor}.png')
        drawer = Draw(image)

        for path in paths:
            drawer.line(path, pen)

        _bytes = BytesIO()
        image.save(_bytes, 'PNG')
        _bytes.seek(0)
        bytes_list.append(_bytes)

    return bytes_list
