from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Parcel


@login_required
def search_parcel(request):
    parcel = None
    searched = False

    if request.method == 'POST':
        reference = request.POST.get('reference')
        searched = True

        try:
            parcel = Parcel.objects.get(reference=reference)
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