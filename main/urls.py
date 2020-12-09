from django.urls import path

from main import views

urlpatterns = [
    path('',  views.Index.as_view(), name="index"),
    path('album/',  views.Albums.as_view(), name="albums"),
    path('album/<str:album_id>', views.Photos.as_view(), name="photos"),
]
