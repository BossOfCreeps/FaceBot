from django.urls import path

from main import views

urlpatterns = [
    path('',  views.Index.as_view(), name="index"),
    path('albums/',  views.Albums.as_view(), name="albums"),
]
