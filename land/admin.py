from django.contrib import admin
from .models import (
    Owner,
    Parcel,
    Document,
    Building,
    AgriculturalZone,
    LandTransaction,
    Report,
    Purchase,
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
        'status',
        'price',
        'for_sale',
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
        'verified',
        'created_at',
    )

    list_filter = (
        'verified',
        'document_type',
        'created_at',
    )

    search_fields = (
        'document_number',
        'parcel__reference',
        'parcel__location',
    )

    ordering = (
        '-created_at',
    )


@admin.register(Building)
class BuildingAdmin(admin.ModelAdmin):

    list_display = (
        'parcel',
        'building_type',
        'description',
    )

    list_filter = (
        'building_type',
    )

    search_fields = (
        'parcel__reference',
        'parcel__location',
        'description',
    )

@admin.register(AgriculturalZone)
class AgriculturalZoneAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'parcel',
        'location',
        'area',
    )

    list_filter = (
        'location',
    )

    search_fields = (
        'name',
        'parcel__reference',
        'location',
        'description',
    )


@admin.register(LandTransaction)
class LandTransactionAdmin(admin.ModelAdmin):

    list_display = (
        'parcel',
        'transaction_type',
        'date',
        'verified',
    )

    list_filter = (
        'transaction_type',
        'verified',
        'date',
    )

    search_fields = (
        'parcel__reference',
        'parcel__location',
        'description',
    )

    ordering = (
        '-date',
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

@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):

    list_display = (
        'parcel',
        'buyer',
        'amount',
        'status',
        'created_at',
        'paid_at',
        'transaction_reference',
    )

    list_filter = (
        'status',
        'created_at',
    )

    search_fields = (
        'parcel__reference',
        'buyer__username',
        'buyer__email',
        'transaction_reference',
    )

    readonly_fields = (
        'created_at',
    )