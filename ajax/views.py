import base64
import io

import face_recognition
from PIL import Image
from django.http import JsonResponse


def is_face(request):
    p = 600
    inmemory_file = io.BytesIO(base64.decodebytes(request.POST["data"][23:].encode()))
    img = Image.open(inmemory_file)
    w, h = img.size
    img.resize((p, int(p * h / w))) if w > h else img.resize((int(p * w / h), p)).save(inmemory_file, "JPEG")
    face_locations = face_recognition.face_locations(face_recognition.load_image_file(inmemory_file))
    return JsonResponse({"face": bool(face_locations)})
