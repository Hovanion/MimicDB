from IntegrinDiagram.integrinDiagram import build_dimer_diagram
from IntegrinDiagram.integrinDiagram import build_dimer_thumbnail
from IntegrinDiagram.integrinDiagram import build_pdb_diagram
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.urls import reverse


# This handler forces all Model and Model fields to be validated before saving.
# See for more info:
# https://docs.djangoproject.com/en/2.0/ref/models/instances/#validating-objects
@receiver(pre_save)
def pre_save_handler(sender, instance, *args, **kwargs):
    instance.full_clean()


class Monomer(models.Model):
    """ A Monomer is a single Alpha or Beta Integrin subunit. The Monomer model
    houses all information which is specific to an Integrin monomer.

    Attributes:
        name (str): A name for the Monomer. e.g.: 'alpha-X'
        uniprot (str): The 6 character Uniprot ID for the subunit
        ensg (str): The 15 character Ensemble Gene ID for the gene
                    corresponding to each monomer
        gene_name (str): A human-friendly gene name
        subunit (str): Subunit type, one of: 'alpha' or 'beta'
        length (int): Length of the Monomner's protein sequence (number of
                      amino acids)
        alpha_interaction_domain (bool, optional): Whether this is an Alpha
                                                   subunit which acts as sole interaction domain. True or
                                                   False for Alpha subunits,
                                                   None for Beta subunits
        sequence (str): The amino acid sequence
        expression (str, optional): A string with expression information from
                                    the Human Protein Atlas
        structure (obj:`MonomerToStructure`): A ManyToMany ForeignKey to the
                                              Structures model, via
                                              intermediary model
                                              MonomerToStructure
        notes (str, optional): Extra information stored as notes

    """

    SUBUNITS = (
        ('alpha', 'alpha'),
        ('beta', 'beta'),
    )

    TAXA = (
        ('Metazoa', 'Metazoa'),
        ('Chordata', 'Chordata'),
    )

    name = models.CharField(max_length=30, unique=True)
    protein = models.OneToOneField(
        "Protein",
        on_delete=models.CASCADE,
    )
    ensg = models.CharField(max_length=15, unique=True)
    gene_name = models.CharField(max_length=30, unique=True)
    subunit = models.CharField(max_length=5, choices=SUBUNITS)
    alpha_interaction_domain = models.NullBooleanField(null=True)
    length = models.IntegerField()
    sequence = models.TextField()
    expression = models.TextField(null=True)
    structure = models.ManyToManyField(
        "Structure",
        through="MonomerToStructure",
    )
    notes = models.TextField(null=True, blank=True)

    def display_name(self):
        """ Return a nicely formatted name as: <alpha.name>/<beta.name>
        """
        if self.subunit == 'alpha':
            return self.name.replace('alpha', 'α').replace('-', '')
        elif self.subunit == 'beta':
            return self.name.replace('beta', 'β').replace('-', '')
        else:
            raise (
                "Invalid subunit value '{0}'. Refusing to continue".format(
                    self.subunit,
                )
            )

    def uniprot_link(self):
        """ Returns a link to the Uniprot entry for this Monomer via the
        Protein model.
        """
        return self.protein.uniprot_link()

    def ensembl_link(self):
        """ Returns a link to the Ensembl entry for this Monomer.
        """
        return "https://www.ensembl.org/id/{0}".format(self.ensg)

    def __str__(self):
        return self.display_name()


class Dimer(models.Model):
    """ A Dimer is a full Integrin complex consisting of a single Alpha and a
    single Beta subunit.

    Attributes:
        name (str): A name for the Dimer. Automatically generated from
            Alpha and Beta subunit names as: <alpha.name>/<beta.name>
        alpha (obj:`Monomer`): ForeignKey to the Monomer model, specifying
                               Alpha subunit
        beta (obj:`Monomer`): ForeignKey to the Monomer model, specifying
                              Beta subunit
        expression (str, optional): A string with expression information from
                                    the Human Protein Atlas
        function (str, optional): Extra information stored as notes
    """

    lookup_name = models.CharField(
        max_length=30,
        unique=True,
        editable=False,
    )
    alpha = models.ForeignKey(
        "Monomer",
        on_delete=models.CASCADE,
        related_name='alpha'
    )
    beta = models.ForeignKey(
        "Monomer",
        on_delete=models.CASCADE,
        related_name='beta'
    )
   
    expression = models.TextField(null=True)
    function = models.TextField(null=True)
    
    

    def display_name(self):
        """ Return a nicely formatted name as: <alpha.name>/<beta.name> (with
        greek caracters)
        """
        return u"{0}/{1}".format(
            self.alpha.name.replace('alpha', 'α').replace('-', ''),
            self.beta.name.replace('beta', 'β').replace('-', ''),
        )

    def save(self, *args, **kwargs):
        """ Custom save to populate the "name" field.
        """
        self.lookup_name = "{0}_{1}".format(self.alpha.name, self.beta.name)
        super(Dimer, self).save(*args, **kwargs)

    def __str__(self):
        return self.display_name()

    class Meta:
        unique_together = (("alpha", "beta"))

    def generate_dimer_diagram(self):
        """ Generates a diagram from the IntegrinDiagram Module
        """
        return build_dimer_diagram(self)

    def generate_dimer_thumbnail(self, filepath):
        """ Generates a png thumbnail from the IntegrinDiagram Module
        """

        build_dimer_thumbnail(self, filepath)

    def get_absolute_url(self):
        return reverse("dimer", args=[self.lookup_name])


class AlternativeName(models.Model):
    """ Alternative Protein names for Monomers.

    Attributes:
        monomer (obj`Monomer`): ForeignKey to the Monomer model
        name (str): An alternative name for the Monomer
    """

    protein = models.ForeignKey(
        "Protein",
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = (("protein", "name"))


class MonomerToStructure(models.Model):
    """ The ManyToMany intermediary model linking Monomers to Structures.

    Attributes:
        monomer (obj`Monomer`): ForeignKey to the Monomer model
        structure (obj`Structure`): ForeignKey to the Structure model
        start (int): start position (amino acid number) of structure, 1 based
        stop (int): stop (last) position (amino acid number) of structure, 1
                    based

    """

    monomer = models.ForeignKey("Monomer", on_delete=models.CASCADE)
    structure = models.ForeignKey("Structure", on_delete=models.CASCADE)
    start = models.IntegerField()
    stop = models.IntegerField()

    def __str__(self):
        return "M2M: {0} / {1}".format(self.monomer, self.structure)

    class Meta:
        unique_together = (("monomer", "structure"))


class Pdb(models.Model):
    """ Protein Database (PDB) information.

    Attributes:
        pdb (str): The 4 character PDB ID
        exp_tech (str):  Experimental technique used
        resolution (float, optional): Resultion
        alpha (obj:`Monomer`): ForeignKey to Monomers model
        beta (obj:`Monomer`): ForeignKey to Monomers model
        alpha_domain (obj:`ManyToMany.Structure`, optional): ManyToMany
            ForeignKey to Structure model.
        beta_domain (obj:`ManyToMany.Structure`, optional): ManyToMany
            ForeignKey to Structure model.
        alpha_chain (str): Series of letters representing PDB Chains.
        beta_chain (str): Series of letters representing PDB Chains.
        protein (obj:`PdbToProtein`, optional): ManyToMany ForeignKey via
            PdbToProtein models
        other_interactors (str, optional): Other interactors.

    See the PdbParser for more information on Parsing these values.
    """

    EXP_TECHS = (
        ('NMR', 'NMR'),
        ('X-ray', 'X-ray'),
        ('Electron microscopy', 'Electron microscopy'),
        ('Model', 'Model'),
    )

    pdb = models.CharField(
        max_length=4,
        unique=True,
        verbose_name='PDB ID',
    )
    exp_tech = models.CharField(
        max_length=20,
        choices=EXP_TECHS,
        verbose_name="Experimental technique",
    )
    resolution = models.FloatField(blank=True, null=True)
    alpha = models.ForeignKey(
        Monomer,
        on_delete=models.CASCADE,
        related_name='pdb_alpha',
        blank=True,
        null=True
    )
    beta = models.ForeignKey(
        Monomer,
        on_delete=models.CASCADE,
        related_name='pdb_beta',
        blank=True,
        null=True
    )
    alpha_domain = models.ManyToManyField(
        'Structure',
        related_name='pdb_alpha_domain',
    )
    beta_domain = models.ManyToManyField(
        'Structure',
        related_name='pdb_beta_domain',
    )
    alpha_chain = models.CharField(max_length=62, blank=True, null=True)
    beta_chain = models.CharField(max_length=62, blank=True, null=True)
    protein = models.ManyToManyField(
        'Protein',
        through="PdbToProtein",
    )
    other_interactors = models.CharField(max_length=512, blank=True, null=True)

    def __str__(self):
        return "PDB: {0}".format(self.pdb)

    def save(self, *args, **kwargs):
        """ Save the model instance.
        Raises:
            ValueError if both 'alpha' and 'beta' are not specified.
        """

        if (self.alpha is None) and (self.beta is None):
            raise ValueError(
                "Pdb needs an Alpha or Beta subunit defined (or both)"
            )
        super(Pdb, self).save(*args, **kwargs)

    def generate_pdb_diagram(self):
        """ Generates a diagram from the IntegrinDiagram Module
        """

        return build_pdb_diagram(self)


class Protein(models.Model):
    """ A Generic Protein class, for (non-integrin) protein information.

    Attributes:
        uniprot (str): The Uniprot ID
        species (str): Species name
    """

    uniprot = models.CharField(max_length=100, default="-")
    peptide = models.CharField(max_length=512, default="-")

    species = models.CharField(max_length=512, default="N/A")

    def uniprot_link(self):
        """ Returns a link to the Uniprot entry for this Monomer.
        """
        return "https://www.uniprot.org/uniprot/{0}".format(self.uniprot)

    def __str__(self):
        """ Return the Uniprot ID.
        """
        return self.uniprot


class PdbToProtein(models.Model):
    """ ManyToMany model betwee Pdb and Protein

    Attributes:
        pdb (obj:`Pdb`): ForeignKey to Pdb model
        protein (obj:`protein`): ForeignKey to Protein model
        chain (str): List of characters represeting Chain ID's
        start (int): start of interaction (amino acid position)
        stop (int): stop of interaction (amino acid position)
    """

    pdb = models.ForeignKey('Pdb', on_delete=models.CASCADE)
    protein = models.ForeignKey('Protein', on_delete=models.CASCADE)
    chains = models.CharField(max_length=62, default="-")
    start = models.IntegerField()
    stop = models.IntegerField()

    def __str__(self):
        return "M2M: {0} / {1}".format(self.pdb, self.protein)

    class Meta:
        unique_together = (("pdb", "protein"))


class Structure(models.Model):
    """ Structures are indivitual domains of the Alpha and Beta subunits. For
    the sake of simplicity, Structures are reffered to by a short abbreviated
    name. This Model houses the full name of the Structure.

    Attributes:
        short (str): Abbreviated Structure name
        name (str):  Full structure name
    """

    short = models.CharField(max_length=10)
    name = models.CharField(max_length=120)

    def __str__(self):
        return self.name


class Drug(models.Model):
    """ A Drug is a small molecule, peptide or protein with a know
    interaction with an Integrin.

    Attributes:
        name (str): The Drug's name
        marketing_name (str, optional): Name underwhich the Drug is marketed
        status (str): Drug's clinical status
        drug_type (str): Type of Drug, options: {cyclic peptide, monoclonal
            antibody, or small molecule}
        administration (str): How the drug is administred
        atc (str): The ATC code for the Drug
        atc_class (str): The ATC class for the Drug
        drugbank (str, optional): The DrugBank ID for the Drug
        dimer: Many2Many key to the Dimer model
        launch_year (int, optional): The year the Drug was launched
        notes (str, optional): Any additional notes.
    """

    DRUG_TYPES = (
        ('cyclic peptide', 'cyclic peptide'),
        ('monoclonal antibody', 'monoclonal antibody'),
        ('small molecule', 'small molecule'),
    )

    name = models.CharField(max_length=30, unique=True)
    marketing_name = models.CharField(max_length=30, blank=True, null=True)
    status = models.CharField(max_length=30)
    drug_type = models.CharField(max_length=30, choices=DRUG_TYPES)
    administration = models.CharField(max_length=30)
    atc = models.CharField(max_length=7, unique=True)
    atc_class = models.CharField(max_length=30)
    drugbank = models.CharField(max_length=7, blank=True, null=True)
    dimer = models.ManyToManyField("Dimer", through="DimerToDrug")
    launch_year = models.IntegerField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    def atc_link(self):
        """ Returns a link to the ATC entry for this Drug
        """
        url = (
            "https://www.whocc.no/atc_ddd_index/?"
            "code={0}&showdescription=yes"
        )
        return url.format(self.atc)

    def drugbank_link(self):
        """ Returns a link to the DrugBanke entry for this Drug
        """
        return "https://www.drugbank.ca/drugs/{0}".format(
            self.drugbank
        )

    def __str__(self):
        return self.name


class DimerToDrug(models.Model):
    """ The ManyToMany intermediary model linking Dimers to Drugs.

    Attributes:
        dimer (obj`dimer`): foreignkey to the dimer model
        drug (obj`drug`): foreignkey to the drug model

    note: making a manytomany model without additional fields is not strictly
    necessary. however, we need to define this model to use in the
    dimertodrugtable, to make sure we can display separate rows for each single
    drug-dimer interaction (instead of a single row for each drug.

    """

    dimer = models.ForeignKey("dimer", on_delete=models.CASCADE)
    drug = models.ForeignKey("Drug", on_delete=models.CASCADE)


class ProteinInteractor(models.Model):
    """ The ProteinInteractor model, to store native and non-native
    protein-integrin interactors.

    Attributes:
        protein (obj: `Protein`): OneToOne key to Protein
        name (str): A human readable name for the Protein
        type_of_evidence(str): plus or negative
        type_of_interaction(str): plus or negative

        function (str): A text description of the ProteinInteractor's
        function.
        start (int): start amino acid position of interaction/motif
        stop (int): stop amino acid position of interaction/motif
        site_definition (str): Text definition of site
        strctural_state(str): Structural state.
        motif (str): The motif sequence
        annotated (bool): Whether or not this interaction has been annotated
        pdb (str): A "|" separated list of PDB structures

    See the ProteinInteractorParser for more information on Parsing these
    values.

    Note: This "pdb" field does not map to the Pdb model. Since a lot of the
    information that is know for Pdb model instances is not know for these,
    there is (for now) no relation bewteen the two. That is why the "pdb" field
    on this model is stored as a simple list of "|" separated PDB IDs.
    """

    protein = models.ForeignKey("Protein", on_delete=models.CASCADE)
    # TODO add comment
    name = models.CharField(max_length=128, default="NA")
    type_of_evidence = models.CharField(max_length=3)
    type_of_interaction = models.CharField(max_length=128, default="NA")
    gene_name = models.CharField(max_length=128, default="NA")
    organism = models.CharField(max_length=128, default="NA")
    construct_boundaries = models.CharField(max_length=128, default="NA")
    interacting_region_boundaries = models.CharField(max_length=128, default="NA")
    oligomerization_state = models.CharField(max_length=128, default="NA")
    motif = models.CharField(max_length=128, default="NA")
    target_integrin = models.CharField(max_length=32, default="NA")
    pubmed = models.CharField(max_length=50, default="NA")
    experimental_method = models.CharField(max_length=512, default="NA")
    eco = models.CharField(max_length=128, default="NA")
    competitor = models.CharField(max_length=512, default="NA")
    interaction_strength = models.CharField(max_length=512, default="NA")
    interaction_strength_numeral = models.CharField(max_length=512, default="NA")
    xref = models.CharField(max_length=512, default="NA")
    notes = models.TextField(default="NA")

    # function = models.TextField()
    # taxonomic_group = models.CharField(max_length=128)
    # start = models.IntegerField()
    # stop = models.IntegerField()
    # site_definition = models.CharField(max_length=512)
    # structural_state = models.CharField(max_length=512)
    # motif = models.CharField(max_length=16)
    # annotated = models.BooleanField()
    # pdb = models.CharField(max_length=4096, null=True, blank=True)

    def __str__(self):
        return "{0}".format(self.protein)

    def save(self, *args, **kwargs):
        """ Custom save to populate the "name" field.

        Raises:
            ValueError if self.name is None
        """
        if self.name is None:
            raise ValueError(
                "'name' cannot be None/empty"
            )
        self.lookup_name = self.name.replace(" ", "_")
        super(ProteinInteractor, self).save(*args, **kwargs)

    # def pdbs_for_links(self):
    #     """ Returns a custom formatted list of PDB ID's from self.pdb, split on
    #     "|", to use to build nicely formatted URL's to PDB.
    #
    #     Returns:
    #         [
    #             (pdb1-A (str), pdb1 (str)),
    #             (pdb2-B (str), pdb2 (str),
    #         ] : a list of self.pdb as a list of tuples.
    #
    #     Each tuple as as the first element the PDB-ID with the chain ID, and
    #     the second element without the chain ID. The first is useful for
    #     displaying, and the second is needed to build a URL to the PDB.
    #
    #     """
    #     if self.pdb is None:
    #         return []
    #
    #     pdbs = [pdb.strip() for pdb in self.pdb.split("|")]
    #     pdbs_pdbs = [(pdb, pdb.split("-")[0]) for pdb in pdbs]
    #     return pdbs_pdbs

    def uniprot_blast_link(self):
        """ Returns a link to the Uniprot BLAST page for this
        ProteinInteractor.
        """
        url = "https://www.uniprot.org/blast/?about={0}[{1}-{2}]&key=Motif"
        return url.format(self.protein.uniprot, self.start, self.stop)

    def uniprot_link(self):
        """ Returns a link to the ECO page for this
        ProteinInteractor's experimental_method.
        """
        url = "https://www.uniprot.org/uniprotkb/{}/entry"
        return url.format(self.protein.uniprot)

    def eco_link(self):
        """ Returns a link to the ECO page for thisProteinInteractor's experimental_method.
        """
        url = "https://www.evidenceontology.org/browse/#{}"
        return url.format(self.eco.replace(":", "_"))

    def elm_link(self):
        """ Returns a link to the ECO page for thisProteinInteractor's experimental_method.
        """  # TODO improve comments
        url = "http://elm.eu.org/instances/{}/"
        return url.format(self.motif)

    def pubmed_link(self):
        """ Returns a link to the Pubmed"""
        url = "https://pubmed.ncbi.nlm.nih.gov/3593230{}"
        return url.format(self.pubmed)


class ProteinInformation(models.Model):
    """ The ProteinInteractor model, to store native and non-native
    protein-integrin interactors.

    Attributes:
        protein (obj: `Protein`): OneToOne key to Protein
        name (str): A human readable name for the Protein
        type_of_evidence(str): plus or negative
        type_of_interaction(str): plus or negative

        function (str): A text description of the ProteinInteractor's
        function.
        start (int): start amino acid position of interaction/motif
        stop (int): stop amino acid position of interaction/motif
        site_definition (str): Text definition of site
        strctural_state(str): Structural state.
        motif (str): The motif sequence
        annotated (bool): Whether or not this interaction has been annotated
        pdb (str): A "|" separated list of PDB structures

    See the ProteinInteractorParser for more information on Parsing these
    values.

    Note: This "pdb" field does not map to the Pdb model. Since a lot of the
    information that is know for Pdb model instances is not know for these,
    there is (for now) no relation bewteen the two. That is why the "pdb" field
    on this model is stored as a simple list of "|" separated PDB IDs.
    """

    protein = models.ForeignKey("Protein", on_delete=models.CASCADE)
    length = models.CharField(max_length=128)
    name = models.CharField(max_length=512)
    alternative_name = models.CharField(max_length=512, default="NA")
    gene_name = models.CharField(max_length=128, default="NA")
    organism_common = models.CharField(max_length=128, default="NA")
    organism_scientific = models.CharField(max_length=512, default="NA")
    function = models.TextField(default="NA")

    def __str__(self):
        return "{0}".format(self.protein)

    def save(self, *args, **kwargs):
        """ Custom save to populate the "name" field.
        Raises:
            ValueError if self.name is None
        """
        if self.name is None:
            raise ValueError(
                "'name' cannot be None/empty"
            )
        self.lookup_name = self.name.replace(" ", "_")
        super(ProteinInformation, self).save(*args, **kwargs)


class DimerToProteinInteractor(models.Model):
    """ The DimerToProteinInteractor models, the ManyToMany model bewteen the
    Dimer and ProteinInteractor models.

    Attributes:
        dimer (obj:`Dimer`): ForeignKey to the Dimer model
        protein_interactor (obj:`ProteinInteractor`): ForeignKey to the
            ProteinInteractor model
        interaction (bool): Whether this is an interaction
        affinity (str, optional): A string represting binding affinity
        pmids (str):  a "|" separated list of PUBMED ID's

    See the ProteinInteractorParser for more information on Parsing these
    values.
    """

    dimer = models.ForeignKey("Dimer", on_delete=models.CASCADE)
    protein_interactor = models.ForeignKey(
        "ProteinInteractor",
        on_delete=models.CASCADE,
    )
    interaction = models.BooleanField()
    affinity = models.CharField(max_length=128, blank=True, null=True)
    pmids = models.CharField(max_length=512)

    def __str__(self):
        return "{0} - {1}".format(
            self.dimer, self.protein_interactor.protein
        )

    def list_of_pmids(self):
        """ Returns a list of PMIDs from self.pmids (which is a "|" separated
        list of PMIDs)
        Returns:
            [pmid1, pmid2, ..]: A list of PMIDs.

        """
        if self.pmids is None:
            return []

        return self.pmids.split("|")
