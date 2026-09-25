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