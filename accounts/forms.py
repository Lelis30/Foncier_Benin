import re

from django import forms
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class RegisterForm(forms.ModelForm):

    first_name = forms.CharField(
        label=_("Prénom"),
        max_length=150,
        required=True
    )

    last_name = forms.CharField(
        label=_("Nom"),
        max_length=150,
        required=True
    )

    username = forms.CharField(
        label=_("Nom d'utilisateur"),
        max_length=150,
        help_text=_("Choisissez un nom d'utilisateur unique.")
    )

    email = forms.EmailField(
        label=_("Adresse e-mail"),
        required=True
    )

    password = forms.CharField(
        widget=forms.PasswordInput,
        label=_("Mot de passe"),
        help_text=_(
            "Minimum 8 caractères avec une majuscule, une minuscule, "
            "un chiffre et un caractère spécial."
        )
    )

    password_confirm = forms.CharField(
        widget=forms.PasswordInput,
        label=_("Confirmer le mot de passe")
    )

    class Meta:
        model = User

        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
        ]

    def clean_password(self):
        password = self.cleaned_data.get('password')

        if len(password) < 8:
            raise forms.ValidationError(
                _("Le mot de passe doit contenir au moins 8 caractères.")
            )

        if not re.search(r'[A-Z]', password):
            raise forms.ValidationError(
                _("Le mot de passe doit contenir au moins une lettre majuscule.")
            )

        if not re.search(r'[a-z]', password):
            raise forms.ValidationError(
                _("Le mot de passe doit contenir au moins une lettre minuscule.")
            )

        if not re.search(r'\d', password):
            raise forms.ValidationError(
                _("Le mot de passe doit contenir au moins un chiffre.")
            )

        if not re.search(r'[^A-Za-z0-9]', password):
            raise forms.ValidationError(
                _("Le mot de passe doit contenir au moins un caractère spécial.")
            )

        return password

    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        if password and password_confirm and password != password_confirm:
            self.add_error(
                'password_confirm',
                _("Les mots de passe ne correspondent pas.")
            )

        return cleaned_data