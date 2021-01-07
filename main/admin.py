from django.contrib import admin

from main.models import Album, Photo, CustomUser

admin.site.register(Album)
admin.site.register(Photo)
admin.site.register(CustomUser)
