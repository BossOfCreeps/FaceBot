import io
from time import sleep

from PIL import Image
from PIL.ImageFilter import BoxBlur
from django.core.files.uploadedfile import InMemoryUploadedFile


def magic_with_image(file, orient, p=600):
    # Resize
    img = Image.open(file)

    if orient == "undefined":
        orient = 0

    if int(orient) == 3:
        img = img.rotate(180, expand=True)
    elif int(orient) == 6:
        img = img.rotate(270, expand=True)
    elif int(orient) == 8:
        img = img.rotate(90, expand=True)

    w, h = img.size
    big_img = img.resize((p, int(p * h / w))) if w < h else img.resize((int(p * w / h), p))
    img = img.resize((p, int(p * h / w))) if w > h else img.resize((int(p * w / h), p))

    # Crop and blur
    width, height = big_img.size
    blurred = big_img.crop(((width - p) / 2, (height - p) / 2, (width + p) / 2, (height + p) / 2)).filter(BoxBlur(20))

    # Compose
    img_w, img_h = img.size
    bg_w, bg_h = blurred.size
    blurred.paste(img, ((bg_w - img_w) // 2, (bg_h - img_h) // 2))

    pic_io = io.BytesIO()
    pic_io.seek(0)
    blurred.save(pic_io, "JPEG")
    return InMemoryUploadedFile(file=pic_io, field_name=None, name=f"{img}.jpg", content_type='image/jpeg', size=(p, p),
                                charset=None)
