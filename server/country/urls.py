from django.urls import path
from country.views import CountryListView, CountryDetailView

urlpatterns = [
    path('all', CountryListView.as_view()),
    path('code/<str:code>/', CountryDetailView.as_view()),
]
