import base64
import io

import face_recognition
from django.http import JsonResponse


def is_face(request):
    inmemory_file = io.BytesIO(base64.decodebytes(request.POST["data"][23:].encode()))
    face_locations = face_recognition.face_locations(face_recognition.load_image_file(inmemory_file))
    del inmemory_file
    return JsonResponse({"face": bool(face_locations)})
