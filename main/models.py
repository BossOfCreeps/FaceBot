from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver

from users.models import CustomUser


class Album(models.Model):
    user = models.ForeignKey(CustomUser, verbose_name="Пользователь", on_delete=models.CASCADE, related_name="albums")
    datetime = models.DateTimeField("Дата и время")

    class Meta:
        verbose_name = verbose_name_plural = "Альбом"

    def __str__(self):
        return f'Альбом пользователя "{self.user}" от "{self.datetime.strftime("%H:%M %d/%m/%Y")}"'

    @property
    def age(self):
        z = {}
        for photo in self.photos.all():
            if photo.age:
                for key, val in photo.age.items():
                    if key in z.keys():
                        z[key] += val / 3
                    else:
                        z[key] = val / 3
        return z

    @property
    def gender(self):
        z = {}
        for photo in self.photos.all():
            if photo.gender:
                for key, val in photo.gender.items():
                    if key in z.keys():
                        z[key] += val / 3
                    else:
                        z[key] = val / 3
        return z

    @property
    def race(self):
        z = {}
        for photo in self.photos.all():
            if photo.race:
                for key, val in photo.race.items():
                    if key in z.keys():
                        z[key] += val / 3
                    else:
                        z[key] = val / 3
        return z


class Photo(models.Model):
    album = models.ForeignKey(Album, verbose_name="Альбом", on_delete=models.CASCADE, related_name="photos")
    photo = models.ImageField("Фото")
    age = models.JSONField("Возраст", null=True, blank=True)
    gender = models.JSONField("Пол", null=True, blank=True)
    race = models.JSONField("Раса", null=True, blank=True)

    class Meta:
        verbose_name = verbose_name_plural = "Фото"

    def __str__(self):
        return f'Фото {self.id} из "{self.album}"'


@receiver(post_delete, sender=Photo)
def submission_delete(sender, instance, **kwargs):
    instance.photo.delete(False)
