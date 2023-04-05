from app.models import ProteinInteractor
from django.shortcuts import render


def DownloadView(request):
    data = ProteinInteractor.objects.all()

    context = {"records": data}

    return render(request, 'app/downloads.html', context)
