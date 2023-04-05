from django.views.generic.detail import DetailView
from django_tables2 import SingleTableView
from django.shortcuts import render
from app.models import Monomer, Dimer, Drug, Pdb, ProteinInteractor
import pandas as pd
import pprint

# List of 'random' example dimers to select from.
RANDOM_EXAMPLE_DIMERS = [
    'alpha-IIb_beta-3',
    'alpha-1_beta-1',
    'alpha-4_beta-1',
    'alpha-4_beta-7',
    'alpha-5_beta-1',
    'alpha-V_beta-3',
    'alpha-V_beta-6',
]

def HomePageView(request):
    """ The home page view.
    """
    dimers = Dimer.objects.all()
    drugs = Drug.objects.all()
    pdbs = Pdb.objects.all()
    protein_interactors = ProteinInteractor.objects.all()

    random_dimer = Dimer.objects.filter(
        lookup_name__in=RANDOM_EXAMPLE_DIMERS,
    ).order_by("?")[0]

    random_dimer_counts = {
        #'interactors': random_dimer.proteininteractor_set.count(),
        'drugs': random_dimer.drug_set.count(),
        'structures': sum([
            random_dimer.alpha.pdb_alpha.count(),
            random_dimer.beta.pdb_beta.count()
        ])
    }

    context = {
        'dimers': dimers,
        'random_dimer': random_dimer,
        'random_dimer_counts': random_dimer_counts,
        'drugs': drugs,
        'pdbs': pdbs,
        'protein_interactors': protein_interactors,
    }

    return render(request, 'app/home.html', context)

