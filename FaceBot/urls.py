from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path, include

from django.conf import settings

urlpatterns = [
    path('', include('main.urls')),
    path('ajax/', include('ajax.urls')),
    path('', include('users.urls')),
    # Modules
    path('admin/', admin.site.urls),
    path('', include('social_django.urls')),
    path('accounts/', include('django.contrib.auth.urls')),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
