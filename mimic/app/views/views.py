from app.models import Dimer
from app.models import Drug
from app.models import Monomer
from app.models import Pdb
from app.models import Protein
from app.models import ProteinInteractor
from app.tables import DimerTable
from app.tables import DrugTable
from app.tables import ProteinInteractorTable
from django.views.generic.detail import DetailView
from django_tables2 import SingleTableView

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


# pylint: disable=too-many-ancestors
class MonomerDetailView(DetailView):
    """ Generic View for Monomers.

    Args:
        name (slug): Expects 'name' to be passed for the database
            lookup to the 'name' field of the Monomber model.
    """

    model = Monomer

    slug_url_kwarg = 'name'
    slug_field = 'name'
    context_object_name = 'monomer'


# pylint: disable=too-many-ancestors
class AlphaDetailView(MonomerDetailView):
    """ A subclass of MonomerDetailView which pre-filters to contain
    only "alpha" Monomers.
    """

    def get_queryset(self):
        queryset = super(AlphaDetailView, self).get_queryset()
        return queryset.filter(
            name__istartswith='alpha'
        )


# pylint: disable=too-many-ancestors
class BetaDetailView(MonomerDetailView):
    """ A subclass of MonomerDetailView which pre-filters to contain
    only "beta" Monomers.
    """

    def get_queryset(self):
        queryset = super(BetaDetailView, self).get_queryset()
        return queryset.filter(
            name__istartswith='beta'
        )


# pylint: disable=too-many-ancestors
class DimerDetailView(DetailView):
    """ Detail view for Dimer objects.
    """

    model = Dimer

    slug_url_kwarg = 'lookup_name'
    slug_field = 'lookup_name'
    context_object_name = 'dimer'


# pylint: disable=too-many-ancestors
class DimerListView(SingleTableView):
    """ Detail view for Dimer objects.
    """

    model = Dimer
    table_class = DimerTable


# pylint: disable=too-many-ancestors
# class PdbListView(SingleTableView):
#     """ List view for Pdb objects.
#     """
#
#     model = Pdb
#     table_class = PdbTable
#     table_pagination = True


# pylint: disable=too-many-ancestors
class PdbDetailView(DetailView):
    """ PdbDetail for Pdb objects.
    """

    model = Pdb

    slug_url_kwarg = 'pdb'
    slug_field = 'pdb'
    context_object_name = 'pdb'


# pylint: disable=too-many-ancestors
class DrugDetailView(DetailView):
    """ Ddrugview for Dimer objects.
    """

    model = Drug

    slug_url_kwarg = 'name'
    slug_field = 'name'
    context_object_name = 'drug'


# pylint: disable=too-many-ancestors
class DrugListView(SingleTableView):
    """ Detail view for Drug objects.
    """

    model = Drug
    table_class = DrugTable


# pylint: disable=too-many-ancestors
class ProteinInteractorDetailView(DetailView):
    """ ProteinInteractor view.

    This view uses the Protein model to fetch data, but as there is a OneToOne
    key between the two, its is possible to do this.

    Its a bit hacking, but it works OK. Main caveats:

    - We need to use protein.protein_interactor on the template
    - This might be a bit less future proof.
    """

    model = Protein

    slug_url_kwarg = 'uniprot'
    slug_field = 'uniprot'
    context_object_name = 'protein'
    template_name = "app/proteininteractor_detail.html"


# pylint: disable=too-many-ancestors
class ProteinInteractorListView(SingleTableView):
    """ List view for ProteinInteractor objects.
    """

    model = ProteinInteractor
    table_class = ProteinInteractorTable
    table_pagination = False
