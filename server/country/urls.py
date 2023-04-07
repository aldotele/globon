from django.urls import path
from country.views import CountryView

urlpatterns = [
    path('all', CountryView.as_view()),
]
