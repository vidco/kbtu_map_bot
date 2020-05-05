from io import BytesIO

from PIL import Image, ImageDraw2


def draw(nodes, floor):
    image = Image.open(f'images/{floor}.png')

    pen = ImageDraw2.Pen(color="red")

    drawer = ImageDraw2.Draw(image)
    drawer.line(nodes, pen)

    _bytes = BytesIO()
    image.save(_bytes, 'PNG')
    _bytes.seek(0)

    return _bytes
