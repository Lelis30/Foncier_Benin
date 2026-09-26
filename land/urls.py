from django.urls import path

from .views import (
    search_parcel,
    report_problem,
    parcel_detail,
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

    path(
        'parcel/<int:parcel_id>/',
        parcel_detail,
        name='parcel_detail'
    ),

]