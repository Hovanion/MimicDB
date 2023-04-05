from app.models import ProteinInteractor
from django.db.models import Q
from django.views.generic import ListView


class SearchView(ListView):
    model = ProteinInteractor
    template_name = "app/search.html"

    def get_queryset(self):  # new
        if self.request.GET:
            query = self.request.GET["q"]
            if query != "":
                object_list = ProteinInteractor.objects.filter(Q(name__icontains=query))
            else:
                object_list = []
        else:
            object_list = {}
        return object_list
