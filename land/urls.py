from django.urls import path
from . import views

from .views import (
    search_parcel,
    report_problem,
    parcel_detail,
    purchase_parcel,
    payment_page,
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

    path(
    'parcel/<int:parcel_id>/payment/',
    payment_page,
    name='payment_page'),

    path(
    'parcel/<int:parcel_id>/payment/<str:method>/confirm/',
    views.confirm_payment,
    name='confirm_payment'
    ),
]