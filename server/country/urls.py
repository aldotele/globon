from django.urls import path
from country.views import CountryList, CountryDetailView, LanguageView

urlpatterns = [
    path('', CountryList.as_view()),
    path('code/<str:code>', CountryDetailView.as_view()),
    path('languages/', LanguageView.as_view()),
]

