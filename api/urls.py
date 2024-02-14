from django.urls import path
from api.views import index, generateCode, stream

urlpatterns = [
    path("", index),
    path("generate-code", generateCode),
    path("test", stream),
]
