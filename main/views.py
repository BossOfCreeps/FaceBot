import base64
import io

from django.contrib.auth import login
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.timezone import now
from django.views import View

from main.lib import magic_with_image
from main.models import Album, Photo


class Index(View):
    def get(self, request, *args, **kwargs):
        login(request, User.objects.first())
        return render(request, "index.html")

    def post(self, request, *args, **kwargs):
        album = Album.objects.create(user=request.user, datetime=now())
        for val in request.POST["data"].split("data:image/jpeg;base64,")[1:]:
            inmemory_file = io.BytesIO(base64.b64decode(val.split('"/><p>')[0].encode()))
            Photo.objects.create(album=album, photo=magic_with_image(inmemory_file))
        return JsonResponse({"album_id": album.id})


class Albums(View):
    def get(self, request, *args, **kwargs):
        return render(request, "albums.html", {"albums": Album.objects.order_by("-datetime")})


class Photos(View):
    def get(self, request, *args, **kwargs):
        return render(request, "photos.html", {"album": Album.objects.get(id=kwargs["album_id"])})
