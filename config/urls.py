from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path,include


urlpatterns = [
    path(settings.ADMIN_URL, admin.site.urls),
    path(settings.API_URL,include("api.urls"))

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
