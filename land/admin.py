from django.contrib import admin
from django.utils import timezone
from django.contrib import messages

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
        'sale_status',
    )

    list_filter = (
        'status',
        'sale_status',
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
        'payment_method',
        'transfer_validated',
    )

    list_filter = (
        'status',
        'created_at',
        'payment_method',
        'transfer_validated',
    )
    actions = ['validate_transfer']

    search_fields = (
        'parcel__reference',
        'buyer__username',
        'buyer__email',
        'transaction_reference',
    )

    readonly_fields = (
        'created_at',
    )

    @admin.action(description="Valider le transfert de propriété")
    def validate_transfer(self, request, queryset):

        for purchase in queryset:

            if purchase.status != 'PAID':
                self.message_user(
                    request,
                    f"Le paiement de {purchase.parcel.reference} n'est pas validé.",
                    level=messages.ERROR
                )
                continue

            if purchase.transfer_validated:
                self.message_user(
                    request,
                    f"Le transfert de {purchase.parcel.reference} a déjà été validé.",
                    level=messages.WARNING
                )
                continue
            if not purchase.parcel.for_sale:
                self.message_user(
                    request,
                    f"La parcelle {purchase.parcel.reference} n'est plus disponible à la vente.",
                    level=messages.ERROR
                )
                continue

            buyer = purchase.buyer

            new_owner, created = Owner.objects.get_or_create(
                email=buyer.email,
                defaults={
                    'first_name': buyer.first_name or buyer.username,
                    'last_name': buyer.last_name or '',
                    'phone': '',
                }
            )
            parcel = purchase.parcel

            parcel.owner = new_owner
            parcel.for_sale = False
            parcel.sale_status = 'SOLD'
            parcel.save(
                update_fields=[
                    'owner',
                    'for_sale',
                    'sale_status',
                ]
            )
            LandTransaction.objects.create(
                parcel=parcel,
                transaction_type='TRANSFER',
                date=timezone.now().date(),
                description=(
                    f"Transfert de propriété validé après paiement "
                    f"{purchase.transaction_reference}. "
                    f"Nouveau propriétaire : {new_owner.first_name} {new_owner.last_name}."
                ),
                verified=True
            )

            purchase.transfer_validated = True
            purchase.transfer_validated_at = timezone.now()

            purchase.save(
                update_fields=[
                    'transfer_validated',
                    'transfer_validated_at'
                ]
            )

            self.message_user(
                request,
                f"Transfert de la parcelle {purchase.parcel.reference} validé.",
                level=messages.SUCCESS
            )