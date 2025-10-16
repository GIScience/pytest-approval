from io import BytesIO

from PIL import Image


def sort_dict(dictionary: dict) -> dict:
    result = {}
    for k, v in sorted(dictionary.items()):
        if isinstance(v, dict):
            result[k] = sort_dict(v)
        else:
            result[k] = v
    return result


def pillow_image_to_bytes(image: Image.Image, extension: str) -> bytes:
    buffer = BytesIO()
    format = extension.replace(".", "")
    if format == "jpg":
        format = "jpeg"
    image.save(buffer, format=format)
    return buffer.getvalue()
