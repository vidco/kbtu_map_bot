from io import BytesIO

from PIL import Image, ImageDraw2


def draw(delimited_path):

    pen = ImageDraw2.Pen(color="red")
    bytes_list = []

    for floor, path in delimited_path.items():
        image = Image.open(f'images/{floor}.png')
        drawer = ImageDraw2.Draw(image)

        for subpath in path:
            drawer.line(subpath, pen)

        _bytes = BytesIO()
        image.save(_bytes, 'PNG')
        _bytes.seek(0)
        bytes_list.append(_bytes)

    return bytes_list
