from django.urls import path
from world_proxy.views import welcome, ready


urlpatterns = [
    path('', welcome, name='welcome'),
    path('ready/', ready, name='ready')
]
