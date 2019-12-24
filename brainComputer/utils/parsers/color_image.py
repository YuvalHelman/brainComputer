from pathlib import Path
from PIL import Image
from brainComputer.utils.parser import ParserContext  # TODO: change to relative (other parsers too )


class colorImageParser:
    field = 'color_image'

    def parse(self, context: ParserContext, snapshot):
        path = context.path("color_image.jpg")
        width, height, data = snapshot.color_image
        image = Image.frombytes('RGB', (width, height), data)

        image.save(path)

# @Parser.parser('color_image')
# def parse_color_image(context, snapshot):
#     p = Path(f"{context.parser_path}/color_image.json")
#     width, height, data = snapshot.color_image
#     image = Image.frombytes('RGB', (width, height), data)
#
#     with open(p, mode="w") as fd:
#         image.save(p)
