from django.urls import path

from ajax import views

urlpatterns = [
    path('',  views.is_face, name="is_face"),
]
