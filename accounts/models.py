from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('USER', 'Utilisateur'),
        ('ADMIN', 'Administrateur'),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='USER'
    )

    phone = models.CharField(
        max_length=20,
        blank=True
    )

    accessibility_mode = models.BooleanField(
        default=False
    )

    def __str__(self):
        return self.user.username


