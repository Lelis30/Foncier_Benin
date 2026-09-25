from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Parcel, Report


@login_required
def search_parcel(request):

    parcel = None
    searched = False

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

            except Parcel.DoesNotExist:
                parcel = None

    return render(
        request,
        'user/parcel_search.html',
        {
            'parcel': parcel,
            'searched': searched
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