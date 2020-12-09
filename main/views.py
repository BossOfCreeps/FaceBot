from django.contrib.auth import login
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.utils.timezone import now
from django.views import View

from main.models import Album, Photo


class Index(View):
    def get(self, request, *args, **kwargs):
        login(request, User.objects.first())
        return render(request, "index.html")

    def post(self, request, *args, **kwargs):
        album = Album.objects.create(user=request.user, datetime=now())

        for file in request.FILES.getlist("img_logo"):
            print(file)
            Photo.objects.create(album=album, photo=file)

        return HttpResponseRedirect("/")


class Albums(View):
    def get(self, request, *args, **kwargs):
        return render(request, "albums.html", {"albums": Album.objects.order_by("datetime")})
