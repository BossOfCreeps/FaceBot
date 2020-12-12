from django.urls import path

from ajax import views

urlpatterns = [
    path('is_face/',  views.is_face, name="is_face"),
    path('delete_album/',  views.delete_album, name="delete_album"),
    path('edit_album/',  views.edit_album, name="edit_album"),
    path('get_album_datetime/', views.get_album_datetime, name="get_album_datetime"),

]
