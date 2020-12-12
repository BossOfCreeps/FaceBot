import base64
import io
from datetime import datetime

from PIL import Image
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from face_recognition import face_locations, load_image_file

from main.models import Album


def is_face(request):
    p = 600
    img_base64_start = "data:image/jpeg;base64,"

    inmemory_file = io.BytesIO(base64.decodebytes(request.POST["data"][23:].encode()))
    img = Image.open(inmemory_file)

    if request.POST["orient"] == "3":
        img = img.rotate(180, expand=True)
    elif request.POST["orient"] == "6":
        img = img.rotate(270, expand=True)
    elif request.POST["orient"] == "8":
        img = img.rotate(90, expand=True)

    w, h = img.size
    img = img.resize((p, int(p * h / w))) if w > h else img.resize((int(p * w / h), p))
    inmemory_file2 = io.BytesIO()
    img.save(inmemory_file2, "JPEG")
    faces = face_locations(load_image_file(inmemory_file2))

    if len(faces) == 0:
        return JsonResponse({"state": False, "text": "No face on image "})
    elif len(faces) > 1:
        return JsonResponse({"state": False, "text": f"{len(faces)} face on image "})
    else:
        (top, right, bottom, left) = faces[0]
        buffered = io.BytesIO()
        img = img.crop((left, top, right, bottom))
        img.save(buffered, format="JPEG")
        return JsonResponse({"state": True, "text": img_base64_start + base64.b64encode(buffered.getvalue()).decode()})


def delete_album(request):
    Album.objects.get(id=request.POST["album_id"]).delete()
    return HttpResponse("")


def edit_album(request):
    album = Album.objects.get(id=request.POST["album_id"])
    album.datetime = datetime.strptime(request.POST["datetime"], "%Y-%m-%dT%H:%M")
    album.save()
    return HttpResponseRedirect(reverse('albums'))


def get_album_datetime(request):
    return JsonResponse({"data": Album.objects.get(id=request.POST["album_id"]).datetime.strftime("%Y-%m-%dT%H:%M")})
