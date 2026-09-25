from django.urls import path

from .views import (
    search_parcel,
    report_problem,
)


urlpatterns = [

    path(
        'search/',
        search_parcel,
        name='search_parcel'
    ),

    path(
        'report/',
        report_problem,
        name='report_problem'
    ),

]