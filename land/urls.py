from django.urls import path

from .views import (
    search_parcel,
    report_problem,
    parcel_detail,
    purchase_parcel,
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

    path(
    'parcel/<int:parcel_id>/purchase/',
    purchase_parcel,
    name='purchase_parcel'
    ),
]