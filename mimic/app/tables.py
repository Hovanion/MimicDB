import django_tables2 as tables

from .models import Dimer
from .models import Drug
from .models import Pdb
from .models import ProteinInteractor


class DimerTable(tables.Table):
    """ A Table with basic Dimer information.
    """

    # name_l = tables.LinkColumn(
    #    'dimer',
    #    args=[tables.utils.A('lookup_name')],
    #    order_by=tables.utils.A('lookup_name'),
    # )
    display_name = tables.LinkColumn(
        'dimer',
        args=[tables.utils.A('lookup_name')],
        order_by=tables.utils.A('lookup_name'),
        verbose_name='Name',
    )
    alpha = tables.LinkColumn(
        'alpha',
        args=[tables.utils.A('alpha.name')],
        verbose_name='α subunit',
    )
    beta = tables.LinkColumn(
        'beta',
        args=[tables.utils.A('beta.name')],
        verbose_name='β subunit',
    )

    class Meta:
        model = Dimer
        fields = ('display_name', 'alpha', 'beta', 'expression')
        attrs = {'class': 'table table-hover'}


class PdbTable(tables.Table):
    """ A Table with basic Pdb information.
    """

    pdb = tables.LinkColumn(
        'pdb',
        args=[tables.utils.A('pdb')],
    )
    alpha = tables.LinkColumn(
        'alpha',
        args=[tables.utils.A('alpha.name')],
        verbose_name='α subunit present',
    )
    beta = tables.LinkColumn(
        'beta',
        args=[tables.utils.A('beta.name')],
        verbose_name='β subunit present',
    )

    proteins = tables.TemplateColumn(
        '{% if record.protein.count %}✔{%else%}—{%endif%}',
        verbose_name='Protein interactors present',
    )
    other_interactors = tables.BooleanColumn(
        'other_interactors',
        verbose_name='Peptide/antibody/drugs present',
    )

    class Meta:
        model = Pdb
        fields = (
            'pdb',
            'exp_tech',
            'resolution',
            'alpha',
            'beta',
            'proteins',
            'other_interactors',
        )
        attrs = {'class': 'table table-hover'}


class DrugTable(tables.Table):
    """ A Table with basic Drug information.
    """

    name = tables.LinkColumn('drug', args=[tables.utils.A('name')])
    dimer = tables.ManyToManyColumn(linkify_item=True)
    drugbank = tables.TemplateColumn(
        '<a target="_blank" href="{{record.drugbank_link}}">'
        '{{record.drugbank}}</a>'
    )

    class Meta:
        model = Drug
        fields = (
            'name',
            'drugbank',
            'marketing_name',
            'launch_year',
            'drug_type',
            'dimer')
        attrs = {'class': 'table table-hover'}


class ProteinInteractorTable(tables.Table):
    """ A Table with basic ProteinInteractor information.
    """

    name = tables.LinkColumn(
        'protein-interactor', args=[tables.utils.A('protein.uniprot')]
    )
    dimer = tables.ManyToManyColumn(linkify_item=True)
    uniprot = tables.TemplateColumn(
        '<a target="_blank" href="{{record.protein.uniprot_link}}">'
        '{{record.protein.uniprot}}</a>'
    )
    motif_location = tables.TemplateColumn(
        '<a target="_blank" href="{{record.uniprot_blast_link}}">'
        '{{record.start}}-{{record.stop}}</a>'
    )
    uniprot = tables.TemplateColumn(
        '<a target="_blank" href="{{record.protein.uniprot_link}}">'
        '{{record.protein.uniprot}}</a>'
    )

    class Meta:
        model = ProteinInteractor
        fields = (
            'name',
            'uniprot',
            'taxonomic_group',
            'site_definition',
            'motif',
            'motif_location',
            'dimer',
        )
        attrs = {'class': 'table table-hover'}
