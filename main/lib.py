from io import BytesIO
from PIL import Image
from PIL.ImageFilter import BoxBlur
from django.core.files.uploadedfile import InMemoryUploadedFile


def magic_with_image(file, p=600):
    # Resize
    img = Image.open(file)
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

    pic_io = BytesIO()
    blurred.save(pic_io, "JPEG")
    return InMemoryUploadedFile(file=pic_io, field_name=None, name=str(file), content_type='image/jpeg', size=(p, p),
                                charset=None)
