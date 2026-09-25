from django.contrib import admin
from .models import (
    Owner,
    Parcel,
    Document,
    Building,
    AgriculturalZone,
    LandTransaction,
    Report
)


@admin.register(Owner)
class OwnerAdmin(admin.ModelAdmin):

    list_display = (
        'first_name',
        'last_name',
        'phone',
        'email'
    )

    search_fields = (
        'first_name',
        'last_name',
        'email'
    )


@admin.register(Parcel)
class ParcelAdmin(admin.ModelAdmin):

    list_display = (
        'reference',
        'owner',
        'location',
        'area',
        'status'
    )

    list_filter = (
        'status',
    )

    search_fields = (
        'reference',
        'location',
    )


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):

    list_display = (
        'document_number',
        'parcel',
        'document_type',
        'verified'
    )

    list_filter = (
        'verified',
        'document_type'
    )


@admin.register(Building)
class BuildingAdmin(admin.ModelAdmin):

    list_display = (
        'parcel',
        'building_type'
    )


@admin.register(AgriculturalZone)
class AgriculturalZoneAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'location',
        'area'
    )


@admin.register(LandTransaction)
class LandTransactionAdmin(admin.ModelAdmin):

    list_display = (
        'parcel',
        'transaction_type',
        'date',
        'verified'
    )


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'parcel',
        'user',
        'status',
        'created_at',
    )

    list_filter = (
        'status',
        'created_at',
    )

    search_fields = (
        'parcel__reference',
        'user__username',
        'description',
    )