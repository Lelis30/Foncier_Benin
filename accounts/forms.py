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
        label=_("Mot de passe")
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

    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        if password != password_confirm:
            raise forms.ValidationError(
                _("Les mots de passe ne correspondent pas.")
            )

        return cleaned_data