from django.contrib.auth.models import User
from django.db import models


class Album(models.Model):
    user = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.CASCADE, related_name="albums")
    datetime = models.DateTimeField("Дата и время")

    class Meta:
        verbose_name = verbose_name_plural = "Альбом"

    def __str__(self):
        return f'Альбом пользователя "{self.user}" от "{self.datetime.strftime("%H:%M %d/%m/%Y")}"'

class Photo(models.Model):
    album = models.ForeignKey(Album, verbose_name="Альбом", on_delete=models.CASCADE, related_name="photos")
    photo = models.ImageField("Фото")
