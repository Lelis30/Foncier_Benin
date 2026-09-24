from django.shortcuts import render, redirect
from django.contrib.auth import (authenticate, login, logout)
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

from .forms import RegisterForm
from .models import UserProfile


def home(request):

    return render(request, 'home.html')


def register(request):

    if request.method == 'POST':

        form = RegisterForm(
            request.POST
        )

        if form.is_valid():

            user = form.save(
                commit=False
            )

            user.set_password(
                form.cleaned_data['password']
            )

            user.save()

            UserProfile.objects.create(
                user=user,
                role='USER'
            )

            login(
                request,
                user
            )

            return redirect(
                'user_dashboard'
            )

    else:

        form = RegisterForm()

    return render(
        request,
        'accounts/register.html',
        {'form': form}
    )


def login_view(request):

    if request.method == 'POST':

        username = request.POST.get(
            'username'
        )

        password = request.POST.get(
            'password'
        )

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(
                request,
                user
            )

            if user.is_staff:

                return redirect(
                    'admin_dashboard'
                )

            return redirect(
                'user_dashboard'
            )

        return render(
            request,
            'accounts/login.html',
            {
                'error':
                'Identifiants incorrects.'
            }
        )

    return render(
        request,
        'accounts/login.html'
    )


def logout_view(request):

    logout(request)

    return redirect(
        'home'
    )


@login_required
def user_dashboard(request):

    return render(
        request,
        'user/dashboard.html'
    )


@staff_member_required
def admin_dashboard(request):

    return render(
        request,
        'admin_dashboard/dashboard.html'
    )
