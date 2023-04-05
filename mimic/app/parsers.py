import re
from io import StringIO
from random import randint

import pandas as pd
from Bio import SeqIO
from app.models import AlternativeName
from app.models import Dimer
from app.models import DimerToDrug
from app.models import Drug
from app.models import Monomer
from app.models import MonomerToStructure
from app.models import Pdb
from app.models import PdbToProtein
from app.models import Protein
from app.models import ProteinInformation
from app.models import ProteinInteractor
from app.models import Structure
from django.core.exceptions import ObjectDoesNotExist


class StructureParser(object):
    """ A parser for Structure objects.

    Attributes:
        filename (str): The name of the file to parse
        messages (list): A list of messages detailing what has been uploaded
            and created when "parse_and_upload" has been run.

    The file should be an excel file, with at least the following two columns:

        - "Domain_shorthand": The shorthand name for the Structure
        - "Domain_name": The full name for the Structure

    The "Domain_shorthand" values should be the same as those used for
    describing the Structure composition of Monomers in the MonomerParser.
    """

    def __init__(self, filename):
        """ Parse and Upload Structures.
        """

        self._filename = filename

        self._data = []
        self.messages = []

    def _upload_row(self, series):
        """ Upload a single row.
        """

        structure = Structure.objects.create(
            short=series['Domain_shorthand'],
            name=series['Domain_name'],
        )

        self.messages.append(
            "Added structure: {0}: {1}".format(
                structure.short, structure.name,
            )
        )

    def _parse_file(self):
        """ Parse the excel file, and store the data in self._data as a pandas
        DataFrame.
        """

        self._data = pd.read_excel(self._filename)

    def parse_and_upload(self):
        """ Parse self._filename and upload all contents.
        """

        # First parse the file and set self._data
        self._parse_file()

        # Upload contents from each row one by one
        for index_series in self._data.iterrows():
            # extract Series from tuple
            series = index_series[1]

            self._upload_row(series)


class MonomerParser(object):
    """ A parser for Monomer objects.

    Attributes:
        filename (str): The name of the file to parse
        messages (list): A list of messages detailing what has been uploaded
            and created when "parse_and_upload" has been run.

    The file should be an excel file, with at least the following two columns:

        - "Integrin_name": The name of the Monomer
        - "UniProt_accession": The 6 character Uniprot ID
        - "Ensemble_accession": The Ensembl Gene Identifier
        - "Gene_name": The canonical gene name
        - "Alternative_names": a list of alternative gene names, each separated
              by a "|"
        - "alpha_interaction_domain": Whether this is an alpha interaction
              domain. Allowed values are 'yes' or 'no' (for alpha subunits) and
              'N/A' for beta subunits.
        - "Domains_and_regions": A list of Structures, separated by "|". Each
              entry should have the structure <short_name>@<start>-<stop>.
        - "Length": The length of the sequence
        - "Sequence": FASTA formattaed string (including header). The newline
              character (including the one after the header) may optionally be
              denoted using "&".
        - "Expression": Text description of HPA expression
        - "Notes": Any extra notes 

    The "short_name" part of the "Domains_and_regions" column should map to
    existing `Structure` instances.
    """

    def __init__(self, filename):
        """
        """

        self._filename = filename

        self._data = []
        self.messages = []

        # By convention, the '&' may be used to denote a newline character in
        # the uploaded fasta.
        self._newline_char = '&'

    @staticmethod
    def _parse_subunit(integrin_name):
        """ Parse the Integrin subunit type ('alpha' or 'beta') from
        'integrin_name'. This function will return 'alpha' if any part of
        integrin_name matches the string 'alpha' (case insensitive), or
        likewise for 'beta'.

        Args:
            integrin_name (str): Contents of the column 'Integrin_name'.

        Returns:
            subunit (str): One of 'alpha' or 'beta'.

        Raises:
            ValueError: If the string 'alpha' or 'beta' (case insensitive) are
                        not found.
        """

        if 'alpha' in integrin_name.lower():
            return 'alpha'
        elif 'beta' in integrin_name.lower():
            return 'beta'

        raise ValueError(
            "Could not determine subunit type from "
            "string: '{0}'".format(integrin_name)
        )

    def _parse_sequence(self, fasta):
        """ Parse the amino acid sequence from FASTA formatted string 'fasta'.

        Args:
            fasta (str): FASTA formatted string

        Returns:
            subunit (str): sequence from FASTA entry
        """

        # Replace newline character
        fasta = fasta.replace(self._newline_char, '\n')

        stringio = StringIO(fasta)
        record = SeqIO.read(stringio, 'fasta')
        return str(record.seq)

    @staticmethod
    def _parse_ensg():
        """ Hack! Need to return some random ENSG, but we probably won't use
        them.
        """

        ensg = "ENSG{0:15d}".format(randint(0, 100000))
        return ensg

    @staticmethod
    def _parse_alpha_interaction_domain(series):
        """ Parse the alpha interaction domain info. Returns `True`, `False` or
        `None`.

        Args:
            alpha_interaction_domain (str): data from the
                alpha_interaction_domain column

        Returns:
            alpha_interaction_domain (bool): Whether or not this is an Alpha
                interaction domain. See below for details.

        This is based on a combined reading of the values of "Integrin_name"
        and "Structures":

        * `True` if the "Integrin_name" contains "alpha" (case insensitive) and
            "Structures" contains "alpha-i" (case insensitive).
        * `False` if the "Integrin_name" contains "alpha" (case insensitive)
            and "Structures" does not contains "alpha-i" (case insensitive).
        * `None` if the "Integrin_name" does not contains "alpha" (case
            insensitive).

        """

        if 'alpha' in series['Integrin_name'].lower():
            if 'alpha-i' in series['Domains_and_regions'].lower():
                return True
            else:
                return False
        return None

    def _get_or_create_human_protein(self, uniprot):
        """ Get or create a protein object where 'uniprot' = uniprot.

        Args:
            uniprot (str): A uniprot ID

        Returns:
            protein (obj:`Protein`): The fetched/created Protein instance

        NOTE: As this is part of the Monomer parser, it automatically tries to
        find or create a Protein with species="Homo sapiens"
        """

        protein, created = Protein.objects.get_or_create(
            uniprot=uniprot,
            species="Homo sapiens",  # TODO before it was human
        )

        return protein

    def _upload_monomer(self, series):
        """ Upload the Monomer instance using data from the row 'series'.

        Args:
            series (obj:`Series`): A pandas Series monomer information.

        Returns:
            monomer (obj:`Monomer`): The created Monomer instance

        See class documentation for information about the contents/structure of
        `series`.
        """

        monomer = Monomer.objects.create(
            name=series['Integrin_name'],
            protein=self._get_or_create_human_protein(
                series['UniProt_accession']
            ),
            ensg=series['Ensembl_accession'],
            gene_name=series['Gene_name'],
            subunit=self._parse_subunit(series['Integrin_name']),
            alpha_interaction_domain=self._parse_alpha_interaction_domain(
                series
            ),
            length=series['Length'],
            sequence=self._parse_sequence(series['Sequence']),
            expression=series['Expression'],
            notes=series['Notes'],
        )

        self.messages.append(
            "Added new Monomer: {0}".format(monomer)
        )

        return monomer

    def _upload_alternative_names(self, protein, series):
        """ Upload the AlternativeNames for 'protein'.

        Args:
            protein (obj:`Protein`): the Protein instance to add
                AlternativeNames for.
            series (obj:`Series`): A pandas Series monomer information.

        See class documentation for information about the contents/structure of
        `series`.
        """

        alternative_names = series['Alternative_names'].split("|")

        # If series['Alternative_names'] is blank, "''", then .split("|")
        # returns a single empty string: ['']. See
        # https://stackoverflow.com/questions/16645083/
        #   when-splitting-an-empty-string-in-python-why-does-split-return-an-empty-list
        # for an example.
        # Clean these up here:
        alternative_names = [a for a in alternative_names if a]

        for name in alternative_names:

            _, created = AlternativeName.objects.get_or_create(
                protein=protein,
                name=name,
            )
            if created:
                self.messages.append(
                    "Created new AlternativeName '{0}' for {1}".format(
                        name, protein,
                    )
                )
            else:
                self.messages.append(
                    "AlternativeName '{0}' already exists for {1}".format(
                        name, protein,
                    )
                )

    def _upload_structures(self, monomer, series):
        """ Upload the Structures for 'monomer'.

        Args:
            monomer (obj:`Monomer`): the Monomer instance to add
                AlternativeName for.
            series (obj:`Series`): A pandas Series monomer information.

        Raises:
            Exception:  if there are issues parsing any structures.

        See class documentation for information about the contents/structure of
        `series`.
        """

        structures = series['Domains_and_regions'].split("|")

        # Format of each entry is "short@start-stop"
        structure_re = re.compile(
            r"(?P<short>\S+)@(?P<start>\d+)-(?P<stop>\d+)"
        )

        for structure_str in structures:

            match = structure_re.match(structure_str)

            if not match:
                raise Exception(
                    "Could not parse structure: '{0}'".format(structure_str)
                )

            structure = Structure.objects.get(short=match.group('short'))

            MonomerToStructure.objects.create(
                monomer=monomer,
                structure=structure,
                start=match.group('start'),
                stop=match.group('stop'),
            )

            # add() does not save, do it manually
            monomer.save()

            self.messages.append(
                "Added new Structure '{0}' to Monomer '{1}'".format(
                    structure, monomer,
                )
            )

    def _upload_row(self, series):
        """ Upload a single row.
        """

        monomer = self._upload_monomer(series)
        self._upload_alternative_names(monomer.protein, series)
        self._upload_structures(monomer, series)

    def _clean_empty_dash(self):
        """ Replace all "-" values in self._data with ""
        """

        self._data.replace("-", "", inplace=True)

    def _parse_file(self):
        """ Parse the excel file, and store the data in self._data
        """

        # Remove default "N/A" converters, we handle these ourselves.
        self._data = pd.read_excel(
            self._filename,
            keep_default_na=False
        )

    def parse_and_upload(self):
        """ Parse self._filename and upload all contents.
        """

        # First parse the file and set self._data
        self._parse_file()

        # Do some cleaning
        self._clean_empty_dash()

        # Upload contents from each row one by one
        for index_series in self._data.iterrows():
            # extract Series from tuple
            series = index_series[1]

            self._upload_row(series)


class DimerParser(object):
    """ A parser for Dimer objects.

    Attributes:
        filename (str): The name of the file to parse
        messages (list): A list of messages detailing what has been uploaded,
            created when "parse_and_upload" has been run.

    The file should be an excel file, with at least the following two columns:

        - "Dimer_name": Dimer name, format: <alpha-name>/<beta-name> 
        - "Expression": Text description of HPA expression 
        - "Notes": Any extra notes 

    The "Dimer_name" values should be the same as those used for `Monomer.name`
    """

    def __init__(self, filename):
        """ Parse and Upload Dimers.
        """

        self._filename = filename

        self._data = []
        self.messages = []

    def _upload_row(self, series):
        """ Upload a single row.
        """

        # Format of each entry is "<alpha-name>/<beta-name>"
        dimer_re = re.compile(
            r"(?P<alpha>\S+)/(?P<beta>\S+)"
        )

        match = dimer_re.match(series['Dimer_name'])

        alpha = Monomer.objects.get(name=match.group('alpha'))
        beta = Monomer.objects.get(name=match.group('beta'))

        Dimer.objects.create(
            alpha=alpha,
            beta=beta,
            expression=series['Expression'],
            notes=series['Notes'],
        )

        self.messages.append(
            "Added Dimer: {0}".format(series['Dimer_name'])
        )

    def _parse_file(self):
        """ Parse the excel file, and store the data in self._data as a pandas
        DataFrame.
        """

        self._data = pd.read_excel(self._filename)

    def parse_and_upload(self):
        """ Parse self._filename and upload all contents.
        """

        # First parse the file and set self._data
        self._parse_file()

        # Upload contents from each row one by one
        for index_series in self._data.iterrows():
            # extract Series from tuple
            series = index_series[1]

            self._upload_row(series)


class PdbParser(object):
    """ A parser for Pdbobjects.

    Attributes:
        filename (str): The name of the file to parse
        messages (list): A list of messages detailing what has been uploaded,
            created when "parse_and_upload" has been run.

    The file should be an excel file, with at the following columns:

    - "PDB_ID": The 4 digit PDB identifier
    - "Resolution": resolution of X-ray and electron microscopy structures,
      measured in Angstroms. For all other techniques, it is 'N/A'.
    - "alpha_subunit": the type of the included alpha integrin subunit (if
      any), followed by ':', followed by the PDB chain ID(s). Only one subunit
      name is allowed. If there is no alpha subunit, use "N/A", "-", or leave
      empty.
    - "alpha_domains": a list of alpha subunit domains visible in the
      structure. Possible domains are defined in the domain_shorthands.xlsx.
      If there are no beta domains, use "N/A", "-", or leave empty.
    - "beta_subunit": the type of the included beta integrin subunit (if any),
      followed by ':', followed by the PDB chain ID(s). Only one subunit name
      is allowed. If there is no beta subunit, use "N/A", "-", or leave empty.
    - "beta_domains – a list of beta subunit domains visible in the
      structure. Possible domains are defined in the domain_shorthands.xlsx
      file are allowed. If there are no beta domains, use "N/A", "-", or leave
      empty.
    - "Protein_interactors": other non-integrin interactors that are present in
      the structure. Two types are defined:
      - "native" the interacting protein is a human protein. It is defined by
        the keyword 'native' followed by a colon, followed the corresponding
        PDB chain ID(s), the UniProt accession, region boundaries, and a
        protein name, all separated by stars ('*'). E.g.:
        'native:CDE*Q96A83*308-329*Collagen alpha-1(XXVI) chain'
      - "non-native" the interacting protein comes from an organism other than
        human. It is defined by the keyword 'non-native' followed by a colon,
        followed the corresponding PDB chain ID(s), the UniProt accession,
        region boundaries, protein name, and the source organism, all separated
        by stars ('*'). E.g.:
        'non-native:A*P84092*159-436*AP-2 complex subunit mu*Rattus norvegicus'
      In case of multiple interaction partners, interactors are separated by
      pipe '|'.
      In case of no protein interactors, use "N/A", "-", or leave empty.
    - "Other_interactors": other interactors that are present in the structure,
      but do not have a UniProt accession for whatever reasons. Four types are
      defined:
      - "peptide" the interacting protein is a (usually synthetic) peptide. It
        is defined by the keyword 'peptide' followed by a colon, followed by
        the PDB chain ID(s), and a free text defining the peptide. E.g.:
        'peptide:BCD:Glogen Peptide'
      - "antibody" the interacting protein is an antibody. It is defined by the
        keyword 'antibody' followed by a colon, followed by the PDB chain
        ID(s), and some free text defining the antibody. E.g.:
        'antibody:H:Monoclonal Antibody Act-1 Heavy Chain'
      - "drug" the interacting protein is an known pharmaceutical agent. It is
        defined by the keyword 'drug' followed by a colon, followed by the PDB
        chain ID(s), some free text defining the drug, and last the canonical
        name of the drug. The drug name (last value) must match the name of
        exactly one drug name from the first column of the integrin_drugs.xlsx
        (A `Drug.name` value). file. E.g.:
        'drug:L:Efalizumab Fab Fragment, Light Chain:Efalizumab'
      - "other": the interacting protein is something that fits none of the
        above definitions. It is defined by the keyword 'other' followed by a
        colon, followed by the PDB chain ID(s), and a free text defining the
        interactor. E.g.: 'other:B:Collagen'
      In case of multiple interaction partners, interactors are separated by
      pipe '|'.
      In case of no protein interactors, use "N/A", "-", or leave empty.
    """

    def __init__(self, filename):
        """ Parse and Upload Dimers.
        """

        self._filename = filename

        self._data = []
        self.messages = []

    def _upload_protein_interactors(self, pdb, series):
        """ Uploads the protein interactors from the series.

        Args:
            pdb (obj:`Pdb`): The Pdb instance to upload for
            series (obj:`pandas.DataSeries`): Containing a
              "Protein_interactors" column.

        Raises:
            Exception:  if there are issues parsing any structures.
        """

        # If there are no Protein_interactors, return
        if series["Protein_interactors"] is None:
            return None

        protein_interactors = series["Protein_interactors"].split("|")

        # Clean up empty strings from list. (see also
        # MonomerParser._upload_alternative_names)
        protein_interactors = [p for p in protein_interactors if p]

        # Format of native entries:
        # native:chains*uniprot*start-stop*name
        # protein_native_re = re.compile(
        #     r"^native:(?P<chains>\w+)\*(?P<uniprot>\w+)\*"
        #     "(?P<start>\d+)-(?P<stop>\d+)\*(?P<name>.*)$"
        # )
        protein_native_re = re.compile(r"^native:(?P<uniprot>\w+)@(?P<start>\d+)-(?P<stop>\d+)\((?P<name>.*)\)$")

        # Format of non-native entries:
        # non-native:chains*uniprot*start-stop*name*species
        # non-native(Foot-and-mouth disease virus - type O*Virus):Q6PMW3@287-933(Genome polyprotein)|non-native(Foot-and-mouth disease virus*Virus):D1H101@202-505(Polyprotein (Fragment))

        protein_non_native_re = re.compile(
            r"^non-native\((?P<name>.*)\):(?P<uniprot>\w+)@"
            "(?P<start>\d+)-(?P<stop>\d+)\((?P<species>.*)\)$"
        )

        for protein_interactor in protein_interactors:

            # Try both regular expressions
            native_match = protein_native_re.match(protein_interactor)
            non_native_match = protein_non_native_re.match(protein_interactor)

            if not (native_match or non_native_match):
                raise Exception(
                    "Could not parse protein interactor: '{0}'".format(
                        protein_interactor
                    )
                )

            if native_match:
                match = native_match
                species = 'Homo sapiens (Human)'
            elif non_native_match:
                match = non_native_match
                species = non_native_match.group('species')

            else:
                raise Exception(
                    "Something wrong, how did we get here?"
                )

            # Get or create the protein
            # protein, _ = Protein.objects.get_or_create(
            #     uniprot=match.group('uniprot'),
            #     species=species,
            # )
            try:
                protein, created = Protein.objects.get_or_create(uniprot=match.group('uniprot'))

            except ObjectDoesNotExist:
                protein = Protein.objects.get_or_create(
                    uniprot=match.group('uniprot'),
                    species=species,
                )

            # print("----protein--->", protein)
            pdb_to_protein = PdbToProtein.objects.create(
                pdb=pdb,
                protein=protein,
                # chains=match.group('chains'),
                start=match.group('start'),
                stop=match.group('stop'),
            )

            pdb_to_protein.save()

    def _upload_other_interactors(self, pdb, series):
        """ Uploads the other interactors from the series.

        Args:
            pdb (obj:`Pdb`): The Pdb instance to upload for
            series (obj:`pandas.DataSeries`): Containing a
              "Other_interactors" column.
        """

        # If there are no Other_interactors, return
        if series["Other_interactors"] is None:
            return None

        other_interactors = series["Other_interactors"].split("|")

        # Clean up empty strings from list. (see also
        # MonomerParser._upload_alternative_names)
        other_interactors = [p for p in other_interactors if p]

        # For now, don't use the list, just save as one long string
        pdb.other_interactors = ",".join(other_interactors)
        pdb.save()

    def _upload_domains(self, pdb, series):
        """ Uploads domains from the series.

        Args:
            pdb (obj:`Pdb`): The Pdb instance to upload for
            series (obj:`pandas.DataSeries`): Containing a
              "Alpha_domains" and/or a "Beta_domains" column(s)
        """

        for monomer in ['Alpha_domains', 'Beta_domains']:

            # skip if None
            if series[monomer] is None:
                continue

            domains = series[monomer].split("|")

            # Clean up empty strings from list. (see also
            # MonomerParser._upload_alternative_names)
            domains = [d for d in domains if d]

            for domain in domains:

                # get the Structure/Domain instance
                structure = Structure.objects.get(short=domain)

                if monomer == 'Alpha_domains':
                    pdb.alpha_domain.add(structure)
                elif monomer == 'Beta_domains':
                    pdb.beta_domain.add(structure)
                else:
                    raise Exception(
                        "Something has gone wrong, how did we get here?"
                    )
                pdb.save()

    def _pdb_parser(self, series):
        """
        Args:
            series (obj:`pandas.DataSeries`: with a "PDB_ID" column
        Returns:
            pdb (str): The value stored in the the "PDB_ID" column.
        """

        return series["PDB_ID"]

    def _exp_tech_parser(self, series):
        """
        Args:
            series (obj:`pandas.DataSeries`: with ab "Exp_tech" column
        Returns:
            exp_tec (str): The value stored in the the "Exp_tech" column.
        """

        return series["Exp_tech"]

    def _resolution_parser(self, series):
        """
        Args:
            series (obj:`pandas.DataSeries`: with a "Resolution" column
        Returns:
            resolution (float): The value stored in the the "Resolution"
              column
            None: None if the value is None 
        """

        if series['Resolution'] is None:
            return None
        return float(series["Resolution"])

    def _monomer_chain_parser(self, series, monomer):
        """
        Args:
            series (obj:`pandas.DataSeries`: with an "Alpha_subunit" column (or
                a "Beta_subunit" column)
            monomer (str): The monomer to parse, one of: "alpha", "beta"
        Returns:
            (Monomer, chain)
                monomer (str): The text before ":" stored in the
                    "alpha_subunit" (or "beta_subunit") column.
                chain (str): The text after ":" stored in the same column.
            (None, None): None if the value is None
        """
        # print("--->", monomer)
        col = "{0}_subunit".format(monomer)
        # print(col)

        # Column names have capital letters
        col = col.capitalize()

        if series[col] is None:
            return (None, None)

        # print(series[col])
        # print("---seriescol>", series[col])
        # name, chain = series[col].split(":")
        name = series[col]
        chain = ""

        monomer = Monomer.objects.get(name=name)

        return (monomer, chain)

    def _upload_row(self, series):
        """ Upload a single row.
        """
        # ("-series-->", series)
        # Uploade the Pdb instance
        pdb = Pdb.objects.create(
            pdb=self._pdb_parser(series),
            exp_tech=self._exp_tech_parser(series),
            resolution=self._resolution_parser(series),
            alpha=self._monomer_chain_parser(series, 'alpha')[0],

            alpha_chain=self._monomer_chain_parser(series, 'alpha')[1],
            beta=self._monomer_chain_parser(series, 'beta')[0],
            beta_chain=self._monomer_chain_parser(series, 'beta')[1],
        )

        # Process Other interactors
        self._upload_domains(pdb, series)

        # Process Protein interactors
        # print(pdb, series)
        self._upload_protein_interactors(pdb, series)

        # Process Other interactors
        self._upload_other_interactors(pdb, series)

        # Add a message
        self.messages.append(
            "Added Pdb: {0}".format(pdb.pdb)
        )

    def _parse_file(self):
        """ Parse the excel file, and store the data in self._data as a pandas
        DataFrame. All 'nan' values are converted to None
        """

        df = pd.read_excel(self._filename, na_values='-')
        self._data = df.where(df.notna(), None)

    def parse_and_upload(self):
        """ Parse self._filename and upload all contents.
        """

        # First parse the file and set self._data
        self._parse_file()

        # Upload contents from each row one by one
        for index_series in self._data.iterrows():
            # extract Series from tuple
            series = index_series[1]

            self._upload_row(series)


class DrugParser(object):
    """ A parser for Drugobjects.

    Attributes:
        filename (str): The name of the file to parse
        messages (list): A list of messages detailing what has been uploaded,
            created when "parse_and_upload" has been run.

    The file should be an excel file, with at least the following two columns:

    - "Name": the standard name of the drug
    - "Marketing_name": the name under which the drug was/is marketed to the
      general public. If none exists, this field should be 'N/A'.
    - "Status": the status of the drug, can be marketed, followed by the
      information if it is prescription only. If the drug has been withdrawn,
      the year of the withdrawal should be indicated.
    - "Type": can be 'cyclic peptide', 'monoclonal antibody', or 'small
      molecule'.
    - "Administration": the standard route of administration for patients.
    - "ATC_code": the code of the drug in the Anatomical Therapeutic Chemical
      (ATC) Classification System.
    - "ATC_definition": the class the drug belongs to, according to ATC
      nomenclature.
    - "Drugbank_ID": the DrugBank ID. If non exists, this field should be ‘N/A’
    - "Target_integrin": integrin(s) the drug is known to bind to. In case of
      multiple integrins, values are separated by pipe '|'.
    - "Lauch_year": the year the drug has entered clinical use (not trials!).
    - "Notes": notes describing the drug.

    The "Dimer_name" values should be the same as those used for `Monomer.name`
    """

    def __init__(self, filename):
        """ Parse and Upload Dimers.
        """

        self._filename = filename

        self._data = []
        self.messages = []

    def _upload_row(self, series):
        """ Upload a single row.

        raises:
            ValueError: if series['Target_integrin'] is empty
        """

        # If "Target_integrin" is empty, splitting by "|" result in an empty
        # string ("") (see also MonomerParser._upload_alternative_names), which
        # will probably result in misleading "DoesNotExist" errors. To avoid
        # this, check here, and raise a clearer Exception.
        if not series["Target_integrin"]:
            raise ValueError("'Target_integrin' cannot be empty")

        # Create the drug object
        drug = Drug.objects.create(
            name=series['Name'],
            marketing_name=series['Marketing_name'],
            status=series['Status'],
            drug_type=series['Type'],
            administration=series['Administration'],
            atc=series['ATC_code'],
            atc_class=series['ATC_definition'],
            drugbank=series['Drugbank_ID'],
            launch_year=series["Launch_year"],
            notes=series['Notes'],
        )

        dimernames = series['Target_integrin'].split("|")

        for dimername in dimernames:
            # Use the lookup_name to retrieve the Dimer object
            lookup_name = dimername.replace("/", "_")
            dimer = Dimer.objects.get(lookup_name=lookup_name)

            # Add the Dimer/Drug interaction
            DimerToDrug.objects.create(
                drug=drug,
                dimer=dimer,
            )

            self.messages.append(
                "Added Integrin Drug: {0} - {1}".format(
                    drug.name,
                    dimer.display_name(),
                )
            )

    def _parse_file(self):
        """ Parse the excel file, and store the data in self._data as a pandas
        DataFrame.
        """

        df = pd.read_excel(self._filename, na_values="-")
        self._data = df.where(df.notna(), None)

    def parse_and_upload(self):
        """ Parse self._filename and upload all contents.
        """

        # First parse the file and set self._data
        self._parse_file()

        # Upload contents from each row one by one
        for index_series in self._data.iterrows():
            # extract Series from tuple
            series = index_series[1]

            self._upload_row(series)


class ProteinInteractorParser(object):
    """ A parser for Interactions.

    Attributes:
        filename (str): The name of the file to parse
        messages (list): A list of messages detailing what has been uploaded,
            created when "parse_and_upload" has been run.

    The file should be an excel file, with the following columns:

    - "Protein_name": the name of the interacting protein taken from UniProt.
    - "Organism": the name of the source organism. If this is human, the
      interactor is native, otherwise it's non-native.

    - "UniProt_accession": the primary accession of the protein
    - "Gene_name": taken from UniProt, always a single run of alphanumeric
      characters
    - "Alternative_names": taken from UniProt, can contain multiple values
      separated by the pipe character ('|')
    - "Function": taken from UniProt, free text
    - "Annotated": Whether or not this interaction has been annotated yet
    This is followed by 3*24 columns, defining the interaction between the
    protein and each of the 24 integrins:
        - one column defines if there is an interaction (header:
          'alpha-x/beta-x', values: '1' for interaction, '0' for
          non-interaction, <blank> for no info)
        - a second column lists references to papers supporting the quoted
          interaction data (header: 'alpha-x/beta-x_ref', values a list of "|"
          separated PMIDs).
        - a third column contains free text describing the binding strength, if
          applicable.
    - "Site_boundaries": location of the core motif in the sequence.
    - "Site_definition": free text from UniProt describing the site
    - "Structural_state": the structural state of the protein around the core
      motif. Can either be 'Ordered' or 'Disordered', followed by the basis of
      the assertion in parentheses. E.g.: Disordered (based on prediction)
    - "Motif_type": a 3-letter definition of the core motif
    - Sub-sequence": the sequence of the core motif, surrounded by 20 residues
      of flanking regions to both sides. If the motif is N- or C-terminal,
      missing residues are marked by dashes '-'.
    - Structures: Structures that contain the interacting region defined in the
      entry. PDB ID followed by dash '-', followed by the chain IDs in the
      structure that represent the interactor. Can contain multiple chain IDs
      concatenated. E.g.: 3C05-AC Can contain multiple structures separated by
      pipe '|'.

    """

    def __init__(self, filename):
        """ Parse and Upload Interactions.
        """

        self._filename = filename

        self._data = []
        self.messages = []

    def _upload_protein(self, series):
        """ Upload the AlternativeNames for 'protein'.

        Args:
            series (obj:`Series`): A pandas Series with ProteinInteractor
                information.

        Returns:
            protein (obj: `Protein): The created/fetched protein object

        See class documentation for information about the contents/structure of
        `series`.
        """

        if series["UniProt accession"] != "-":
            protein, created = Protein.objects.get_or_create(
                uniprot=series['UniProt accession'].strip(),
            )
        else:
            protein, created = Protein.objects.get_or_create(
                uniprot=series['UniProt accession'].strip(),
                peptide=series['Peptide name'].strip(),
            )
        if created:
            self.messages.append(
                "Created new Protein '{0}'".format(protein)
            )
        else:
            self.messages.append(
                "Protein '{0}' already exists in the Protein table".format(protein)
            )
        return protein

    def _upload_protein_interactor(self, protein, series):
        """ Upload the ToProteinInteractor objects.

        Args:
            protein (obj:`Protein`): the Protein instance to add
                AlternativeNames for.
            series (obj:`Series`): A pandas Series with ProteinInteractor
                information.

        Returns:
            protein_interactor (obj:`ProteinInteractor`): The created/fetched
                ProteinInteractor object.

        See class documentation for information about the contents/structure of
        `series`.
        """
        # print("Protein---->", protein)
        protein_intractor, created = ProteinInteractor.objects.get_or_create(
            protein=protein,
            type_of_interaction=series['Type of interaction'],
            type_of_evidence=series['Type of evidence (positive / negative)'],
            construct_boundaries=series['Construct boundaries'],
            interacting_region_boundaries=series['Interacting region boundaries'],
            oligomerization_state=series['Oligomerization state'],
            motif=series['ELM link (if motif mediated)'],
            target_integrin=series['Target integrin'],
            pubmed=series['PubMed ID'],
            experimental_method=series['Experimental method'],
            eco=series['ECO accession'],
            competitor=series['Competitor (if applicable)'],
            interaction_strength=series['Interaction strength (Kd, IC50, etc)'],
            interaction_strength_numeral=series['Interaction strength in nM, single value'],
            xref=series['Xref for bound structure (if applicable)'],
            notes=series['Notes']
        )
        # ("created")
        if created:
            self.messages.append(
                "Added ProteinInteractor' {0}'".format(protein_intractor))
        else:
            self.messages.append(
                "ProteinInteractor '{0}' already exists, no need to create".format(
                    protein_intractor,
                )
            )

        return protein_intractor

    def _upload_row(self, series):
        """ Upload a single row.
        """

        # Fetch or create the protein object.
        protein = self._upload_protein(series)

        # Handle AlternativeNames
        # self._upload_alternative_names(protein, series)

        # Create and save the ProteinInteractor object
        protein_intractor = self._upload_protein_interactor(protein, series)

        # Add DimerToProteinInteractor instances
        # self._upload_dimer_to_protein_interactors(protein_intractor, series)

    def _parse_file(self):
        """


         Parse the excel file, and store the data in self._data as a pandas
        DataFrame.
        """

        df = pd.read_excel(self._filename, na_values="-")
        self._data = df.where(df.notna(), "-")
        # print ("_parse_file")

    # print(self._data)

    def parse_and_upload(self):
        """ Parse self._filename and upload all contents.
        """
        # First parse the file and set self._data
        self._parse_file()

        # Upload contents from each row one by one
        for index_series in self._data.iterrows():
            series = index_series[1]
            # print(series)  # extract Series from tuple

            self._upload_row(series)


class ProteinInformationParser(object):
    """ A parser for Interactions.
    #TODO rewrite description

    """

    def __init__(self, filename):
        """ Parse and Upload Interactions.
        """

        self._filename = filename

        self._data = []
        self.messages = []

    def _upload_protein(self, series):
        """ Upload the AlternativeNames for 'protein'.

        Args:
            series (obj:`Series`): A pandas Series with ProteinInteractor
                information.

        Returns:
            protein (obj: `Protein): The created/fetched protein object

        See class documentation for information about the contents/structure of
        `series`.
        """

        # protein, created = Protein.objects.get_or_create(
        #     uniprot=series['Accession'],
        #     species=series['Organism_scientific'],
        # )

        try:
            protein = Protein.objects.get(uniprot=series['Accession'])

        except ObjectDoesNotExist:
            protein, created = Protein.objects.get_or_create(
                uniprot=series['Accession'],
                species=series['Organism_scientific'],
            )

        # print("---->", protein, created)

        # if created:
        #     self.messages.append(
        #         "Created new Protein '{0}'".format(protein)
        #     )
        # else:
        #     self.messages.append(
        #         "Protein '{0}' already exists in the Protein table".format(protein)
        #     )

        return protein

    def _upload_protein_information(self, protein, series):
        """ Upload the ToProteinInteractor objects.

        Args:
            protein (obj:`Protein`): the Protein instance to add
                AlternativeNames for.
            series (obj:`Series`): A pandas Series with ProteinInteractor
                information.

        Returns:
            protein_interactor (obj:`ProteinInteractor`): The created/fetched
                ProteinInteractor object.

        See class documentation for information about the contents/structure of
        `series`.
        """

        protein_information, created = ProteinInformation.objects.get_or_create(
            protein=protein,
            length=series['Length'],
            name=series['Protein_name'],
            alternative_name=series['Protein_name_alternative'],
            gene_name=series['Gene_name'],
            organism_scientific=series['Organism_scientific'],
            organism_common=series['Organism_common'],
            function=series['Function'],
        )

        if created:
            self.messages.append(
                "Added ProteinInformation' {0}'".format(protein_information))
        else:
            self.messages.append(
                "ProteinInformation '{0}' already exists, no need to create".format(
                    protein_information,
                )
            )

        return protein_information

    def _upload_row(self, series):
        """ Upload a single row.
        """

        # Fetch or create the protein object.
        protein = self._upload_protein(series)

        # Handle AlternativeNames
        # self._upload_alternative_names(protein, series)

        # Create and save the ProteinInformation object
        protein_information = self._upload_protein_information(protein, series)

    def _parse_file(self):
        """ Parse the excel file, and store the data in self._data as a pandas
        DataFrame.
        """

        df = pd.read_excel(self._filename, na_values="-")
        self._data = df.where(df.notna(), "-")
        print ("_parse_file")

    # print(self._data)

    def parse_and_upload(self):
        """ Parse self._filename and upload all contents.
        """
        # First parse the file and set self._data
        self._parse_file()

        # Upload contents from each row one by one
        for index_series in self._data.iterrows():
            series = index_series[1]  # extract Series from tuple
            # print(series)
            self._upload_row(series)
