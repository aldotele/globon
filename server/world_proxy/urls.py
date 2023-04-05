from django.urls import path
from world_proxy.views import welcome


urlpatterns = [
    path('', welcome, name='welcome'),
]
