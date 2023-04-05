from django.shortcuts import render
from app.models import ProteinInteractor
import pprint


def AboutView(request):

    data = ProteinInteractor.objects.values_list('protein', 'protein__uniprot', 'name', 'organism',
                                                 'type_of_interaction').distinct()
    context={'records':list()}

    for row in data:
        adat = {"protein": row[1]}
        adat["name"] = row[2]
        adat["organism"] = row[3]
        adat["type_of_interaction"] = row[4]
        expmethod = ProteinInteractor.objects.filter(protein=row[0]).values_list(
            "experimental_method").distinct().order_by("experimental_method")
        adat["experimental_method"] = ', '.join(str(item[0]) for item in expmethod)
        integrins = ProteinInteractor.objects.filter(protein=row[0]).values_list(
            "target_integrin").distinct().order_by("target_integrin")
        adat["integrins"] = ', '.join(str(item[0]) for item in integrins)
        # print(adat)
        context['records'].append(adat)

    return render(request, 'app/browser.html', context)
