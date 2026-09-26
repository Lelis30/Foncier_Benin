from django.shortcuts import render, redirect
from django.contrib.auth import (authenticate, login, logout)
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .forms import RegisterForm
from .models import UserProfile
from land.models import Parcel, Report, AgriculturalZone

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

    parcels = Parcel.objects.select_related('owner').all()

    parcels_data = []

    for parcel in parcels:


        if parcel.owner:
            owner_name = f"{parcel.owner.first_name} {parcel.owner.last_name}"
        else:
            owner_name = "Non renseigné"

        parcels_data.append({
            'id': parcel.id,
            'reference': parcel.reference,
            'location': parcel.location,
            'area': parcel.area,
            'latitude': parcel.latitude,
            'longitude': parcel.longitude,
            'status': parcel.status,
            'status_display': parcel.get_status_display(),
            'owner': owner_name,
        })

    # ZONES AGRICOLES

    agricultural_zones = AgriculturalZone.objects.all()

    agricultural_zones_data = []

    for zone in agricultural_zones:
        agricultural_zones_data.append({
            'id': zone.id,
            'name': zone.name,
            'location': zone.location,
            'area': zone.area,
            'description': zone.description,
            'latitude': zone.latitude,
            'longitude': zone.longitude,
        })
    return render(
        request,
        'user/dashboard.html',
        {
            'parcels_data': parcels_data,
            'agricultural_zones_data': agricultural_zones_data,
        }
    )



@login_required
def admin_dashboard(request):

    # Seuls les administrateurs
    # peuvent accéder à cette page
    if not request.user.is_staff:
        return redirect('user_dashboard')

    # Tous les signalements
    reports = (
        Report.objects
        .select_related('parcel', 'user')
        .order_by('-created_at')
    )

    # Statistiques
    total_reports = reports.count()

    pending_reports = reports.filter(
        status='PENDING'
    ).count()

    reviewing_reports = reports.filter(
        status='REVIEWING'
    ).count()

    resolved_reports = reports.filter(
        status='RESOLVED'
    ).count()

    # PARCELLES POUR LE TABLEAU DE BORD ADMIN

    parcels = (
        Parcel.objects
            .select_related('owner')
            .order_by('-created_at')
    )

    total_parcels = parcels.count()

    verified_parcels = parcels.filter(
        status='VERIFIED'
    ).count()

    pending_parcels = parcels.filter(
        status='PENDING'
    ).count()

    disputed_parcels = parcels.filter(
        status='DISPUTED'
    ).count()
    return render(
        request,
        'admin_dashboard/dashboard.html',
        {
            'reports': reports,
            'total_reports': total_reports,
            'pending_reports': pending_reports,
            'reviewing_reports': reviewing_reports,
            'resolved_reports': resolved_reports,
            # Parcelles
            'parcels': parcels,
            'total_parcels': total_parcels,
            'verified_parcels': verified_parcels,
            'pending_parcels': pending_parcels,
            'disputed_parcels': disputed_parcels,
        }
    )