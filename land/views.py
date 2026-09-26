from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Parcel, Report, LandTransaction


@login_required
def search_parcel(request):

    parcel = None
    searched = False
    transactions = []

    if request.method == 'POST':

        reference = request.POST.get(
            'reference',
            ''
        ).strip()

        searched = True

        if reference:

            try:

                parcel = (
                    Parcel.objects
                    .select_related('owner')
                    .get(reference__iexact=reference)
                )

                # Transactions :
                # de la plus récente à la plus ancienne
                transactions = (
                    parcel.landtransaction_set
                    .all()
                    .order_by('-date')
                )

            except Parcel.DoesNotExist:

                parcel = None

    return render(
        request,
        'user/parcel_search.html',
        {
            'parcel': parcel,
            'searched': searched,
            'transactions': transactions,
        }
    )


@login_required
def report_problem(request):

    parcels = Parcel.objects.all().order_by('reference')

    success = False

    if request.method == 'POST':

        parcel_id = request.POST.get('parcel')
        description = request.POST.get(
            'description',
            ''
        ).strip()

        if parcel_id and description:

            try:

                parcel = Parcel.objects.get(
                    id=parcel_id
                )

                Report.objects.create(
                    parcel=parcel,
                    user=request.user,
                    description=description,
                    status='PENDING'
                )

                success = True

            except Parcel.DoesNotExist:
                pass

    return render(
        request,
        'user/report_problem.html',
        {
            'parcels': parcels,
            'success': success
        }
    )

@login_required
def parcel_detail(request, parcel_id):

    parcel = get_object_or_404(
        Parcel.objects.select_related('owner'),
        id=parcel_id
    )

    documents = parcel.documents.all()

    transactions = LandTransaction.objects.filter(
        parcel=parcel
    ).order_by('-date')

    buildings = parcel.buildings.all()

    agricultural_zones = parcel.agricultural_zones.all()

    return render(
        request,
        'user/parcel_detail.html',
        {
            'parcel': parcel,
            'documents': documents,
            'transactions': transactions,
            'buildings': buildings,
            'agricultural_zones': agricultural_zones,
        }
    )

@login_required
def parcel_detail(request, parcel_id):

    parcel = get_object_or_404(
        Parcel.objects.select_related('owner'),
        id=parcel_id
    )

    documents = parcel.documents.all()

    transactions = (
        parcel.landtransaction_set
        .all()
        .order_by('-date')
    )

    buildings = parcel.buildings.all()

    agricultural_zones = parcel.agricultural_zones.all()

    return render(
        request,
        'user/parcel_detail.html',
        {
            'parcel': parcel,
            'documents': documents,
            'transactions': transactions,
            'buildings': buildings,
            'agricultural_zones': agricultural_zones,
        }
    )

@login_required
def purchase_parcel(request, parcel_id):

    parcel = get_object_or_404(
        Parcel,
        id=parcel_id
    )

    if not parcel.for_sale or parcel.price is None:
        return render(
            request,
            'user/purchase_unavailable.html',
            {
                'parcel': parcel
            }
        )

    return render(
        request,
        'user/purchase_confirm.html',
        {
            'parcel': parcel
        }
    )