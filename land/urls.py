from django.urls import path
from .views import search_parcel

urlpatterns = [
    path(
        'search/',
        search_parcel,
        name='search_parcel'
    ),
]