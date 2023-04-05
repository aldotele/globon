from django.urls import path
from world_proxy.views import welcome, populate_db_with_countries


urlpatterns = [
    path('', welcome, name='welcome'),
    path('populate', populate_db_with_countries, name='populate'),
]
