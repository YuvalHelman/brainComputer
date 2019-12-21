from pathlib import Path
import json


def parse_translation(context, snapshot):
    p = Path(f"{context.parser_path}/translation.json")
    x, y, z = snapshot.translation

    with open(p, mode="w") as fd:
        fd.write(json.dumps({"x": x, "y": y, "z": z}))


parse_translation.field = 'pose'
