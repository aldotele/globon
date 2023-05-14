from django.urls import path
from country.views import CountryList, LanguageView

urlpatterns = [
    path('', CountryList.as_view()),
    path('languages/', LanguageView.as_view()),
]

