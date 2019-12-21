from pathlib import Path
from PIL import Image


def parse_color_image(context, snapshot):
    p = Path(f"{context.parser_path}/color_image.json")
    width, height, data = snapshot.color_image
    image = Image.frombytes('RGB', (width, height), data)

    with open(p, mode="w") as fd:
        image.save(p)
