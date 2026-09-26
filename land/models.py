from django.db import models
from django.contrib.auth.models import User


class Owner(models.Model):

    first_name = models.CharField(
        max_length=100
    )

    last_name = models.CharField(
        max_length=100
    )

    phone = models.CharField(
        max_length=30,
        blank=True
    )

    email = models.EmailField(
        blank=True
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Parcel(models.Model):

    STATUS_CHOICES = [
        ('VERIFIED', 'Vérifiée'),
        ('PENDING', 'En attente'),
        ('DISPUTED', 'En litige'),

    ]
    SALE_STATUS_CHOICES = [
        ('AVAILABLE', 'Disponible'),
        ('RESERVED', 'Réservée - paiement effectué'),
        ('SOLD', 'Vendue'),
    ]

    reference = models.CharField(
        max_length=50,
        unique=True
    )

    owner = models.ForeignKey(
        Owner,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    location = models.CharField(
        max_length=255
    )

    area = models.FloatField(
        help_text="Superficie en m²"
    )

    latitude = models.FloatField()

    longitude = models.FloatField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='PENDING'
    )

    price = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Prix de vente"
    )

    for_sale = models.BooleanField(
        default=False,
        verbose_name="À vendre"
    )

    sale_status = models.CharField(
        max_length=20,
        choices=SALE_STATUS_CHOICES,
        default='AVAILABLE',
        verbose_name="État de la vente"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.reference


class Document(models.Model):

    DOCUMENT_TYPES = [
        ('TITLE', 'Titre foncier'),
        ('SALE', 'Acte de vente'),
        ('TRANSFER', 'Acte de cession'),
        ('OTHER', 'Autre'),
    ]

    parcel = models.ForeignKey(
        Parcel,
        on_delete=models.CASCADE,
        related_name='documents'
    )

    document_type = models.CharField(
        max_length=30,
        choices=DOCUMENT_TYPES
    )

    document_number = models.CharField(
        max_length=100
    )

    document_file = models.FileField(
        upload_to='documents/',
        blank=True,
        null=True
    )

    verified = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.document_number


class Building(models.Model):

    BUILDING_TYPES = [
        ('HOUSE', 'Maison'),
        ('SHOP', 'Commerce'),
        ('OFFICE', 'Bureau'),
        ('OTHER', 'Autre'),
    ]

    parcel = models.ForeignKey(
        Parcel,
        on_delete=models.CASCADE,
        related_name='buildings'
    )

    building_type = models.CharField(
        max_length=30,
        choices=BUILDING_TYPES
    )

    description = models.TextField(
        blank=True
    )

    def __str__(self):
        return self.building_type


class AgriculturalZone(models.Model):

    # Parcelle liée à la zone agricole
    parcel = models.ForeignKey(
        Parcel,
        on_delete=models.CASCADE,
        related_name='agricultural_zones',
        null=True,
        blank=True
    )

    # Nom de la zone
    name = models.CharField(
        max_length=200
    )

    # Localisation
    location = models.CharField(
        max_length=255
    )

    # Superficie en m²
    area = models.FloatField()

    # Description
    description = models.TextField(
        blank=True
    )

    # Coordonnées GPS
    latitude = models.FloatField()

    longitude = models.FloatField()

    def __str__(self):
        return self.name


class LandTransaction(models.Model):

    TRANSACTION_TYPES = [
        ('SALE', 'Vente'),
        ('TRANSFER', 'Cession'),
        ('INHERITANCE', 'Héritage'),
    ]

    parcel = models.ForeignKey(
        Parcel,
        on_delete=models.CASCADE
    )

    transaction_type = models.CharField(
        max_length=30,
        choices=TRANSACTION_TYPES
    )

    date = models.DateField()

    description = models.TextField()

    verified = models.BooleanField(
        default=False
    )

    def __str__(self):
        return f"{self.parcel.reference} - {self.transaction_type}"


class Report(models.Model):

    STATUS_CHOICES = [
        ('PENDING', 'En attente'),
        ('REVIEWING', 'En cours de vérification'),
        ('RESOLVED', 'Résolu'),
    ]

    parcel = models.ForeignKey(
        Parcel,
        on_delete=models.CASCADE
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    description = models.TextField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='PENDING'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"Signalement #{self.id}"

class Purchase(models.Model):

    STATUS_CHOICES = [
        ('PENDING', 'En attente de paiement'),
        ('PAID', 'Payé'),
        ('CANCELLED', 'Annulé'),
    ]

    PAYMENT_METHOD_CHOICES = [
        ('MTN', 'MTN Mobile Money'),
        ('MOOV', 'Moov Money'),
        ('CARD', 'Carte bancaire'),
    ]

    parcel = models.ForeignKey(
        Parcel,
        on_delete=models.PROTECT,
        related_name='purchases'
    )

    buyer = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='land_purchases'
    )

    amount = models.DecimalField(
        max_digits=15,
        decimal_places=2
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='PENDING'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    paid_at = models.DateTimeField(
        null=True,
        blank=True
    )

    transaction_reference = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )
    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHOD_CHOICES,
        blank=True,
        null=True
    )
    transfer_validated = models.BooleanField(
        default=False,
        verbose_name="Transfert de propriété validé"
    )

    transfer_validated_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Date de validation du transfert"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['parcel', 'buyer'],
                name='unique_purchase_per_parcel_buyer'
            )
        ]

    def __str__(self):
        return f"{self.parcel.reference} - {self.buyer.username} - {self.status}"
