import random
import string
import factory

from app.models import Monomer
from app.models import Structure
from app.models import MonomerToStructure
from app.models import Pdb
from app.models import Dimer
from app.models import AlternativeName
from app.models import Drug
from app.models import DimerToDrug
from app.models import Protein
from app.models import PdbToProtein
from app.models import ProteinInteractor
from app.models import DimerToProteinInteractor


AMINO_ACIDS = "ACDEFGHIKLMNPQRSTVWY"
CHARACTERS = string.ascii_uppercase + string.ascii_lowercase + string.digits
SUBUNITS = ['alpha', 'beta']
DRUG_TYPES = ('cyclic peptide', 'monoclonal antibody', 'small molecule')
EXP_TECHS = ('NMR', 'X-ray', 'Electron microscopy', 'Model')
SPECIES = ["Homo sapiens", "Mus musculus", "Naja naja"]


def random_aa_string(length=10):
    """ Return a random string selected from AMINO_ACIDS.
    """

    letters = [random.choice(AMINO_ACIDS) for i in range(length)]
    return ''.join(letters)


def random_string(length=10):
    """ Return a random string selected from CHARACTERS.
    """

    letters = [random.choice(CHARACTERS) for i in range(length)]
    return ''.join(letters)


def random_ensembl(prefix):
    """ Return a random ensembl-like identifier.

    Args:
        prefix (str):   For example: "ENSG"
    """

    return "{0}{1}".format(prefix, random_string(11))


def random_pdb_list(length=5):
    """ Generate a string of PDBs separated by "|"
    Args:
        legth (int): Number of PDB IDs to include
    Returns:
        pbds (list): List of PDB ids (with chain IDs)
    """
    pdbs = []

    for _ in range(random.randint(0,length)):
        pdbs.append("{0}-{1}".format(
            random_string(4),
            random_string(1),
            )
        )
    return "|".join(pdbs)


def random_pmid_list(length=5):
    """ Generate a string of PMIDs separated by "|"
    Args:
        legth (int): Number of PMID IDs to include
    Returns:
        pmids (list): List of PMIDs
    """
    pmids = []

    for _ in range(length):
        pmids.append(str(random.randint(0, 1000000)))
    return "|".join(pmids)


def character_generator():
    """ A generator that yields a combination of non-repeating characters.

    yields: All contents of CHARACTERS, followed by all pairwise combinations
        of characters in CHARACTERS
    """

    # Create a list of all pairwise combinations as strings
    combinations = [''.join([a, b]) for a in CHARACTERS for b in CHARACTERS]

    for a in list(CHARACTERS) + combinations:
        yield a
    raise Exception(
        "character_generator ran out of letters."
    )

# Use this to generate characters to use as Monomer suffixes when creating a
# name. e.g.: "alpha-{0}".format(next(monomer_suffix_generator))
monomer_suffix_generator = character_generator()


class StructureFactory(factory.DjangoModelFactory):
    """ ModelFactory for Structure objects.
    """

    short = factory.LazyAttribute(lambda t: random_string(4))
    name = factory.LazyAttribute(lambda t: random_string(12))

    class Meta:
        model = Structure


class MonomerFactory(factory.DjangoModelFactory):
    """ ModelFactory for Monomer objects.

    Note: Monomers are created without any assigned structures. To create a
    Monomer object with a single structure, do one of the following 2 methods:

    Use the MonomerWithStructureFactory object:

    >>> from factories import MonomerWithStructureFactory
    >>> m = MonomerWithStructureFactory.create()

    Or, create them by hand via the MonomerToStructure object:

    >>> from factories import MonomerFactory, StructureFactory
    >>> from models import MonomerToStructure
    >>> s = StructureFactory.create()
    >>> m = MonomerFactory.create()
    >>> MonomerToStructure.objects.create(monomer=m, structure=s, start=1,
            stop=100)

    Note: Monomers are also not created with AlternativeName objects. To add
    one, do:

    >>> from factories import MonomerFactory, AlternativeNameFactory
    >>> a = AlternativeNameFactory.create()
    >>> m = MonomerFactory.create()
    >>> m.alternativename_set.add(a)
    """

    name = factory.LazyAttribute(
        lambda t: "{0}-{1}".format(t.subunit, next(monomer_suffix_generator))
    )
    protein = factory.SubFactory('app.tests.factories.ProteinFactory')
    ensg = factory.LazyAttribute(lambda t: random_ensembl("ENSG"))
    gene_name = factory.LazyAttribute(lambda t: random_string(8))
    subunit = factory.LazyAttribute(lambda t: random.choice(SUBUNITS))
    alpha_interaction_domain = factory.LazyAttribute(
        lambda t: random.choice([True, False])
    )
    length = factory.LazyAttribute(lambda t: random.randint(100, 500))
    sequence = factory.LazyAttribute(lambda t: random_aa_string(t.length))
    expression = factory.LazyAttribute(lambda t: random_string(60))
    notes = factory.LazyAttribute(lambda t: random_string(160))

    class Meta:
        model = Monomer


class AlphaFactory(MonomerFactory):
    """ ModelFactory that produces "alpha" Monomer instances.
    """
    subunit = 'alpha'


class BetaFactory(MonomerFactory):
    """ ModelFactory that produces "Beta" Monomer instances.
    """
    subunit = 'beta'


class DimerFactory(factory.DjangoModelFactory):
    """ ModelFactory for Dimer objects.
    """

    lookup_name = factory.LazyAttribute(
        lambda t: "{0}_{1}".format(t.alpha.name, t.beta.name)
    )
    alpha = factory.SubFactory(AlphaFactory)
    beta = factory.SubFactory(BetaFactory)
    expression = factory.LazyAttribute(lambda t: random_string(60))
    notes = factory.LazyAttribute(lambda t: random_string(160))

    class Meta:
        model = Dimer


class AlternativeNameFactory(factory.DjangoModelFactory):
    """ ModelFactory for AlternativeName objects.
    """

    protein = factory.SubFactory('app.tests.factories.ProteinFactory')
    name = factory.LazyAttribute(lambda t: random_string(10))

    class Meta:
        model = AlternativeName


class MonomerToStructureFactory(factory.DjangoModelFactory):
    """ ModelFactory for MonomerToStructure objects.
    """

    monomer = factory.SubFactory(MonomerFactory)
    structure = factory.SubFactory(StructureFactory)
    start = factory.LazyAttribute(lambda t: random.randint(0, 100))
    stop = factory.LazyAttribute(lambda t: random.randint(0, 100))

    class Meta:
        model = MonomerToStructure


class MonomerWithStructureFactory(MonomerFactory):
    """ ModelFactory for Monomer with a single Structure.
    """

    structure = factory.RelatedFactory(MonomerToStructureFactory, 'monomer')


class PdbFactory(factory.DjangoModelFactory):
    """ ModelFactory for Pdb objects.

    Pdb's are linked to Structures (a.k.a. Domains) via a ManyToMany
    ForeignKey. Structures are added via the "post_generation" hook, which
works as follows:

    >>> a,b,c = StructureFactory.create_batch(3)
    >>> p = PdbFactory.create(beta_domain=(a,b,c))

    Otherwise, add them by hand:

    >>> s = StructureFactory.create()
    >>> p = PdbFactory.create()
    >>> p.beta_domain.add(s)

    """

    pdb = factory.LazyAttribute(lambda t: random_string(4))
    exp_tech = factory.LazyAttribute(lambda t: random.choice(EXP_TECHS))
    resolution = factory.LazyAttribute(lambda t: random.random()*3)
    alpha = factory.SubFactory(AlphaFactory)
    beta = factory.SubFactory(BetaFactory)
    alpha_chain = factory.LazyAttribute(
        lambda t: random_string(random.randint(1, 10))
    )
    beta_chain = factory.LazyAttribute(
        lambda t: random_string(random.randint(1, 10))
    )

    class Meta:
        model = Pdb

    @factory.post_generation
    def alpha_domain(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of structures/domains were passed in, use them
            for domain in extracted:
                self.alpha_domain.add(domain)

    @factory.post_generation
    def beta_domain(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of structures/domains were passed in, use them
            for domain in extracted:
                self.beta_domain.add(domain)


class ProteinFactory(factory.DjangoModelFactory):
    """ ModelFactory for Protein objects.
    """

    uniprot = factory.LazyAttribute(lambda t: random_string(6))
    species = factory.LazyAttribute(lambda t: random.choice(SPECIES))

    class Meta:
        model = Protein


class PdbToProteinFactory(factory.DjangoModelFactory):
    """ ModelFactory for a PdbToProtein objects
    """

    pdb = factory.SubFactory(PdbFactory)
    protein = factory.SubFactory(ProteinFactory)
    chains = factory.LazyAttribute(
        lambda t: random_string(random.randint(1, 3))
    )
    start = factory.LazyAttribute(lambda t: random.randint(0, 100))
    stop = factory.LazyAttribute(lambda t: random.randint(0, 100))

    class Meta:
        model = PdbToProtein


class DrugFactory(factory.DjangoModelFactory):
    """ ModelFactory for Drugs objects.

    Dimer objects are linked to drugs via a ManytoMany relationship. See
    MonomerFactory for information on how to link objects defined via a
    ManyToMany relationship.

    """

    name = factory.LazyAttribute(lambda t: random_string(12))
    marketing_name = factory.LazyAttribute(lambda t: random_string(12))
    status = factory.LazyAttribute(lambda t: random_string(24))
    drug_type = factory.LazyAttribute(lambda t: random.choice(DRUG_TYPES))
    administration = factory.LazyAttribute(lambda t: random_string(24))
    atc = factory.LazyAttribute(lambda t: random_string(7))
    atc_class = factory.LazyAttribute(lambda t: random_string(12))
    drugbank = factory.LazyAttribute(lambda t: random_string(7))
    launch_year = factory.LazyAttribute(lambda t: random.randint(1900, 2018))
    notes = factory.LazyAttribute(lambda t: random_string(240))

    class Meta:
        model = Drug


class DimerToDrugFactory(factory.DjangoModelFactory):
    """ ModelFactory for DrugToDimer objects.
    """

    drug = factory.SubFactory(DrugFactory)
    dimer = factory.SubFactory(DimerFactory)

    class Meta:
        model = DimerToDrug


class ProteinInteractorFactory(factory.DjangoModelFactory):
    """ ModelFactory for ProteinInteractor objects.
    """

    protein = factory.SubFactory(ProteinFactory)
    name = factory.LazyAttribute(lambda t: random_string(12))
    function = factory.LazyAttribute(lambda t: random_string(120))
    taxonomic_group = factory.LazyAttribute(lambda t: random_string(12))
    start = factory.LazyAttribute(lambda t: random.randint(0, 100))
    stop = factory.LazyAttribute(lambda t: random.randint(100, 200))
    site_definition = factory.LazyAttribute(lambda t: random_string(120))
    structural_state = factory.LazyAttribute(lambda t: random_string(120))
    motif = factory.LazyAttribute(lambda t: random_string(5))
    annotated = 0  # by default, False, set to True manually if needed
    pdb = factory.LazyAttribute(lambda t: random_pdb_list())

    class Meta:
        model = ProteinInteractor


class DimerToProteinInteractorFactory(factory.DjangoModelFactory):
    """ ModelFactory for ProteinInteractor objects.
    """

    dimer = factory.SubFactory(DimerFactory)
    protein_interactor = factory.SubFactory(
        ProteinInteractorFactory, annotated=True
    )
    interaction = factory.LazyAttribute(
        lambda t: bool(random.randint(0, 1))
    )
    affinity = factory.LazyAttribute(lambda t: random_string(12))
    pmids = factory.LazyAttribute(
        lambda t: random_pmid_list(random.randint(1, 5))
    )

    class Meta:
        model = DimerToProteinInteractor
