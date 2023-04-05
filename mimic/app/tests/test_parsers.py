# from io import StringIO
# from django.core.management import call_command
# from django.test import TestCase
# from app.models import Monomer
# from app.models import Structure
# from app.models import Dimer
# from app.models import Drug
# from app.models import Pdb
# from app.models import AlternativeName
# from app.tests.factories import AlphaFactory
# from app.tests.factories import BetaFactory
# from app.tests.factories import DimerFactory
# from app.tests.factories import PdbFactory
# from django.core.exceptions import ValidationError
# from django.conf import settings
# from django.db.utils import IntegrityError
# import os
#
#
# def prefix_abs_base_path(path):
#     """ Build and return 'path', prefixed with the value of settings.BASE_PATH
#     (where settings.py lives).
#     """
#
#     return os.path.join(settings.BASE_DIR, path)
#
#
# class DimerParserTest(TestCase):
#     """ Test DimerParser Management Command.
#     """
#
#     def setUp(self):
#         self._out = StringIO()
#
#         # Delete all data
#         call_command('delete_all_integrins', stdout=self._out)
#
#         # Upload structures shorthands
#         call_command(
#             'upload_structures',
#             prefix_abs_base_path('test-data/domain_shorthands.xlsx'),
#             stdout=self._out,
#         )
#
#         # Upload Monomers
#         call_command(
#             'upload_monomers',
#             prefix_abs_base_path('test-data/integrin_monomers_ok.xlsx'),
#             stdout=self._out,
#         )
#
#     def test_upload_ok(self):
#         """ Test that we can upload a Dimer correctly.
#         """
#
#         # Upload Dimer
#         call_command(
#             'upload_dimers',
#             prefix_abs_base_path('test-data/integrin_dimers_ok.xlsx'),
#             stdout=self._out,
#         )
#
#         # Check that it was added
#         expected = "Added Dimer: alpha-X/beta-2"
#         self.assertIn(
#             expected,
#             self._out.getvalue(),
#             msg="Could not find '{0}' in management output.".format(expected),
#         )
#
#     def test_upload_missing_alpha_name(self):
#         """ Test that Dimers cannot be uploaded if Monomer does not exist.
#         """
#
#         # Upload monomers and check raise an error
#         expected = 'Monomer matching query does not exist.'
#
#         fname = prefix_abs_base_path(
#             'test-data/integrin_dimers_UNMATCHED_ALPHA_NAME.xlsx'
#         )
#
#         with self.assertRaisesRegexp(Monomer.DoesNotExist, expected):
#             call_command(
#                 'upload_dimers',
#                 fname,
#                 stdout=self._out,
#             )
#
# class MomomerParserTest(TestCase):
#     """ Test MomomerParser Management Command.
#     """
#
#     def setUp(self):
#         self._out = StringIO()
#
#         # Delete all data
#         call_command('delete_all_integrins', stdout=self._out)
#
#         # Upload structures shorthands
#         call_command(
#             'upload_structures',
#             prefix_abs_base_path('test-data/domain_shorthands.xlsx'),
#             stdout=self._out,
#         )
#
#     def test_upload_ok(self):
#         """ Test that we can upload a Momomer correctly.
#         """
#
#         # Upload Monomers
#         call_command(
#             'upload_monomers',
#             prefix_abs_base_path('test-data/integrin_monomers_ok.xlsx'),
#             stdout=self._out,
#         )
#
#         expected = "Added new Monomer: αX"
#         self.assertIn(
#             expected,
#             self._out.getvalue(),
#             msg="Could not find '{0}' in management output.".format(expected),
#         )
#
#     def test_upload_missing_gene_name(self):
#         """ Raise ValidationError when upload a Momomer with missing GeneName.
#         """
#
#         # Expect this in the output
#         expected = (
#             '.*This field cannot be blank.*'
#         )
#         fname = prefix_abs_base_path(
#             'test-data/integrin_monomers_MISSING_GENE_NAME.xlsx'
#         )
#
#         # Try to upload Monomers
#         with self.assertRaisesRegexp(ValidationError, expected):
#             call_command(
#                 'upload_monomers',
#                 fname,
#                 stdout=self._out,
#             )
#
#     def test_upload_missing_uniprot(self):
#         """ Raise ValidationError when upload a Momomer with missing uniprot
#         ID.
#         """
#
#         # Expect this in the output
#         expected = (
#             '.*This field cannot be blank.*'
#         )
#         fname = prefix_abs_base_path(
#             'test-data/integrin_monomers_MISSING_UNIPROT.xlsx'
#         )
#
#         # Try to upload Monomers
#         with self.assertRaisesRegexp(ValidationError, expected):
#             call_command(
#                 'upload_monomers',
#                 fname,
#                 stdout=self._out,
#             )
#
#     def test_upload_missing_sequence(self):
#         """ Raise ValueError when upload a Momomer with missing sequence.
#         """
#
#         # Expect this in the output
#         expected = (
#             "No records found in handle"
#
#         )
#         fname = prefix_abs_base_path(
#             'test-data/integrin_monomers_MISSING_SEQUENCE.xlsx'
#         )
#
#         # Try to upload Monomers
#         with self.assertRaisesRegexp(ValueError, expected):
#             call_command(
#                 'upload_monomers',
#                 fname,
#                 stdout=self._out,
#             )
#
#     def test_upload_missing_ensemble_gene_id(self):
#         """ Raise error when upload a Momomer with missing ENSEMBL Gene ID.
#         """
#
#         # Expect this in the output
#         expected = (
#             '.*This field cannot be blank.*'
#         )
#         fname = prefix_abs_base_path(
#             'test-data/integrin_monomers_MISSING_ENSEMBLE_GENE_ID.xlsx'
#         )
#
#         # Try to upload Monomers
#         with self.assertRaisesRegexp(ValidationError, expected):
#             call_command(
#                 'upload_monomers',
#                 fname,
#                 stdout=self._out,
#             )
#
#     def test_upload_unmached_domain(self):
#         """ Test that we cannot upload a Momomer with an unmached domain.
#         """
#
#         # Expect this in the output
#         expected = (
#             "Structure matching query does not exist."
#
#         )
#         fname = prefix_abs_base_path(
#             'test-data/integrin_monomers_UNMATCHED_DOMAIN.xlsx'
#         )
#
#         # Try to upload Monomers
#         with self.assertRaisesRegexp(Structure.DoesNotExist, expected):
#             call_command(
#                 'upload_monomers',
#                 fname,
#                 stdout=self._out,
#             )
#
#     def test_upload_no_alternative_empty(self):
#         """ Test that we can upload with an empty AlternativeName.
#         """
#
#         fname = prefix_abs_base_path(
#             'test-data/integrin_monomers_ALTERNATIVE_NAME_EMPTY.xlsx'
#         )
#
#         # Upload monomers
#         call_command(
#             'upload_monomers',
#             fname,
#             stdout=self._out,
#         )
#
#         alpha = Monomer.objects.get(name='alpha-X')
#
#         alternative_names = alpha.protein.alternativename_set.all()
#
#         self.assertEqual(
#             alternative_names.count(), 0,
#             msg="Expected 0 AlteranativeNames."
#         )
#
#     def test_upload_no_alternative_dash(self):
#         """ Test that we can upload with an an empty ('-') AlternativeName.
#         """
#
#         fname = prefix_abs_base_path(
#             'test-data/integrin_monomers_ALTERNATIVE_NAME_DASH.xlsx'
#         )
#
#         # Upload monomers
#         call_command(
#             'upload_monomers',
#             fname,
#             stdout=self._out,
#         )
#
#         alpha = Monomer.objects.get(name='alpha-X')
#
#         alternative_names = alpha.protein.alternativename_set.all()
#
#         self.assertEqual(
#             alternative_names.count(), 0,
#             msg="Expected 0 AlteranativeNames."
#         )
#
#
# class PdbParserTest(TestCase):
#     """ Test PdbParser Management Command.
#     """
#
#     def setUp(self):
#         self._out = StringIO()
#
#         # Delete all data
#         call_command('delete_all_integrins', stdout=self._out)
#
#         # Upload structures shorthands
#         call_command(
#             'upload_structures',
#             prefix_abs_base_path('test-data/domain_shorthands.xlsx'),
#             stdout=self._out,
#         )
#
#         # Upload Monomers
#         call_command(
#             'upload_monomers',
#             prefix_abs_base_path('test-data/integrin_monomers_ok.xlsx'),
#             stdout=self._out,
#         )
#
#         # Upload Dimers
#         call_command(
#             'upload_dimers',
#             prefix_abs_base_path('test-data/integrin_dimers_ok.xlsx'),
#             stdout=self._out,
#         )
#
#     def test_upload_ok_response(self):
#         """ Test that we get the expected output from 'upload_pdbs' management
#         command.
#         """
#
#         # Upload Pdbs
#         call_command(
#             'upload_pdbs',
#             prefix_abs_base_path('test-data/integrin_structures_ok.xlsx'),
#             stdout=self._out,
#         )
#
#         expected = "Added Pdb: 2vdo"
#
#         self.assertIn(
#             expected,
#             self._out.getvalue(),
#             msg="Could not find '{0}' in management output.".format(expected),
#         )
#
#     def test_upload_ok(self):
#         """ Test that we can upload a Pdb correctly.
#         """
#
#         # Add some random Pdb instances
#         PdbFactory.create_batch(3)
#
#         # Upload Pdbs
#         call_command(
#             'upload_pdbs',
#             prefix_abs_base_path('test-data/integrin_structures_ok.xlsx'),
#             stdout=self._out,
#         )
#
#         pdbs = Pdb.objects.filter(
#             pdb='2vdo',
#             exp_tech='X-ray',
#             resolution=2.51,
#             alpha__name='alpha-X',
#             beta__name='beta-2',
#         )
#
#         self.assertEqual(
#             pdbs.count(),
#             1,
#             "Retrieved {0} uploaded Pdbs, expected 1".format(pdbs.count())
#         )
#
#     def test_upload_one_protein_interactor_parser_ok(self):
#         """ Test that we can upload a Pdb with one Protein_interactor, and that
#         parsed values are correct.
#         """
#
#         # Add some random Pdb instances
#         PdbFactory.create_batch(3)
#
#         # Upload Pdbs
#         call_command(
#             'upload_pdbs',
#             prefix_abs_base_path('test-data/integrin_structures_ok.xlsx'),
#             stdout=self._out,
#         )
#
#         pdbs = Pdb.objects.filter(
#             pdb='2vdo',
#             protein__uniprot='P02679',
#             protein__species='Homo sapiens (Human)',
#             pdbtoprotein__chains='C',
#             pdbtoprotein__start=426,
#             pdbtoprotein__stop=434,
#         )
#
#         self.assertEqual(
#             pdbs.count(),
#             1,
#             "Retrieved {0} uploaded Pdbs, expected 1".format(pdbs.count())
#         )
#
#     def test_upload_two_protein_interactor_parser_ok(self):
#         """ Test that we can upload a Pdb with two Protein_interactors
#         correctly, and that parsed values are correct. One is native, one is
#         non-native.
#         """
#
#         # Add some random Pdb instances
#         PdbFactory.create_batch(3)
#
#         # Create filename
#         fname = prefix_abs_base_path(
#             'test-data/integrin_structures_TWO_PROTEIN_INTERACTORS.xlsx'
#         )
#
#         # Upload Pdbs
#         call_command('upload_pdbs', fname, stdout=self._out)
#
#         # Check native protein
#         pdbs = Pdb.objects.filter(
#             pdb='2vdo',
#             protein__uniprot='P02679',
#             protein__species='Homo sapiens (Human)',
#             pdbtoprotein__chains='C',
#             pdbtoprotein__start=426,
#             pdbtoprotein__stop=434,
#         )
#
#         self.assertEqual(
#             pdbs.count(),
#             1,
#             "Retrieved {0} uploaded Pdbs, expected 1".format(pdbs.count())
#         )
#
#         # Check non-native protein
#         pdbs = Pdb.objects.filter(
#             pdb='2vdo',
#             protein__uniprot='P12346',
#             protein__species='Naja naja',
#             pdbtoprotein__chains='C',
#             pdbtoprotein__start=100,
#             pdbtoprotein__stop=1304,
#         )
#
#         self.assertEqual(
#             pdbs.count(),
#             1,
#             "Retrieved {0} uploaded Pdbs, expected 1".format(pdbs.count())
#         )
#
#     def test_upload_missing_pdb_id(self):
#         """ Raise ValidationError when upload a Pdb with no PDB_ID.
#         """
#
#         # Expect this in the output
#         expected = (
#             '.*This field cannot be null.*'
#         )
#         fname = prefix_abs_base_path(
#             'test-data/integrin_structures_MISSING_PDB_ID.xlsx'
#         )
#
#         # Try to upload Pdbs
#         with self.assertRaisesRegexp(ValidationError, expected):
#             call_command(
#                 'upload_pdbs',
#                 fname,
#                 stdout=self._out,
#             )
#
#     def test_upload_missing_exp_tech(self):
#         """ Raise ValidationError when upload a Pdb with no exp_tech.
#         """
#
#         # Expect this in the output
#         expected = (
#             '.*This field cannot be null.*'
#         )
#         fname = prefix_abs_base_path(
#             'test-data/integrin_structures_MISSING_EXP_TECH.xlsx'
#         )
#
#         # Try to upload Pdbs
#         with self.assertRaisesRegexp(ValidationError, expected):
#             call_command(
#                 'upload_pdbs',
#                 fname,
#                 stdout=self._out,
#             )
#
#     def test_upload_missing_other_interactors_ok(self):
#         """ Upload a Pdb with no other_interactors is OK.
#         """
#
#         # Expect this in the output
#         expected = (
#             '.*This field cannot be null.*'
#         )
#
#         fname = prefix_abs_base_path(
#             'test-data/integrin_structures_MISSING_OTHER_INTERACTORS.xlsx'
#         )
#
#         # Upload Pdbs
#         call_command('upload_pdbs', fname, stdout=self._out)
#
#         expected = "Added Pdb: 2vdo"
#
#         self.assertIn(
#             expected,
#             self._out.getvalue(),
#             msg="Could not find '{0}' in management output.".format(expected),
#         )
#
#     def test_upload_missing_protein_interactors_ok(self):
#         """ Upload a Pdb with no protein_interactors is OK.
#         """
#
#         # Expect this in the output
#         expected = (
#             '.*This field cannot be null.*'
#         )
#         fname = prefix_abs_base_path(
#             'test-data/integrin_structures_MISSING_PROTEIN_INTERACTORS.xlsx'
#         )
#
#         # Upload Pdbs
#         call_command('upload_pdbs', fname, stdout=self._out)
#
#         expected = "Added Pdb: 2vdo"
#
#         self.assertIn(
#             expected,
#             self._out.getvalue(),
#             msg="Could not find '{0}' in management output.".format(expected),
#         )
#
#     def test_upload_missing_resolution_ok(self):
#         """ Upload a Pdb with no resolution is OK.
#         """
#
#         # Expect this in the output
#         expected = (
#             '.*This field cannot be null.*'
#         )
#         fname = prefix_abs_base_path(
#             'test-data/integrin_structures_MISSING_RESOLUTION.xlsx'
#         )
#
#         # Upload Pdbs
#         call_command('upload_pdbs', fname, stdout=self._out)
#
#         expected = "Added Pdb: 2vdo"
#
#         self.assertIn(
#             expected,
#             self._out.getvalue(),
#             msg="Could not find '{0}' in management output.".format(expected),
#         )
#
#     def test_upload_missing_resolution_na_ok(self):
#         """ Upload a Pdb if 'N/A' is used for missing (non-required) value.
#         """
#
#         fname = prefix_abs_base_path(
#             'test-data/integrin_structures_MISSING_RESOLUTION_NA.xlsx'
#         )
#
#         # Upload Pdbs
#         call_command('upload_pdbs', fname, stdout=self._out)
#
#         expected = "Added Pdb: 2vdo"
#
#         self.assertIn(
#             expected,
#             self._out.getvalue(),
#             msg="Could not find '{0}' in management output.".format(expected),
#         )
#
#     def test_upload_missing_resolution_hypen_ok(self):
#         """ Upload a Pdb if '-' is used for missing (non-required) value.
#         """
#
#         fname = prefix_abs_base_path(
#             'test-data/integrin_structures_MISSING_RESOLUTION_NA.xlsx'
#         )
#
#         # Upload Pdbs
#         call_command('upload_pdbs', fname, stdout=self._out)
#
#         expected = "Added Pdb: 2vdo"
#
#         self.assertIn(
#             expected,
#             self._out.getvalue(),
#             msg="Could not find '{0}' in management output.".format(expected),
#         )
#
#     def test_upload_missing_alpha_and_beta(self):
#         """ Return ValidationError when alpha and beta subunit are missing
#         """
#
#         # Expect this in the output
#         expected = (
#             '.*Pdb needs an Alpha or Beta subunit defined \(or both\).*'
#         )
#
#         fname = prefix_abs_base_path(
#             'test-data/integrin_structures_MISSING_BETA_AND_ALPHA_SUBUNIT.xlsx'
#         )
#
#         # Try to upload Pdbs
#         with self.assertRaisesRegexp(ValueError, expected):
#             call_command(
#                 'upload_pdbs',
#                 fname,
#                 stdout=self._out,
#             )
#
#     def test_upload_unmatched_alpha(self):
#         """ Return Monomer.DoesNotExist when alpha subunit does not exist.
#         """
#
#         # Expect this in the output
#         expected = (
#             '.*Monomer matching query does not exist.*'
#         )
#         fname = prefix_abs_base_path(
#             'test-data/integrin_structures_UNMATCHED_ALPHA.xlsx'
#         )
#
#         # Try to upload Pdbs
#         with self.assertRaisesRegexp(Monomer.DoesNotExist, expected):
#             call_command(
#                 'upload_pdbs',
#                 fname,
#                 stdout=self._out,
#             )
#
#     def test_upload_unmatched_alpha_domain(self):
#         """ Return Structure.DoesNotExist when an alpha Structure/Domain does
#         not exist.
#         """
#
#         # Expect this in the output
#         expected = (
#             '.*Structure matching query does not exist.*'
#         )
#         fname = prefix_abs_base_path(
#             'test-data/integrin_structures_UNMATCHED_ALPHA_DOMAIN.xlsx'
#         )
#
#         # Try to upload Pdbs
#         with self.assertRaisesRegexp(Structure.DoesNotExist, expected):
#             call_command(
#                 'upload_pdbs',
#                 fname,
#                 stdout=self._out,
#             )
#
#     def test_upload_alpha_only_ok(self):
#         """ Upload a Pdb with only an alpha subunit is OK.
#         """
#
#         # Expect this in the output
#         expected = (
#             '.*This field cannot be null.*'
#         )
#         fname = prefix_abs_base_path(
#             'test-data/integrin_structures_ALPHA_SUBUNIT_ONLY.xlsx'
#         )
#
#         # Upload Pdbs
#         call_command('upload_pdbs', fname, stdout=self._out)
#
#         expected = "Added Pdb: 2vdo"
#
#         self.assertIn(
#             expected,
#             self._out.getvalue(),
#             msg="Could not find '{0}' in management output.".format(expected),
#         )
#
#     def test_upload_one_alpha_domain_ok(self):
#         """ Upload a Pdb with a single Alpha_domain is OK.
#         """
#
#         fname = prefix_abs_base_path(
#             'test-data/integrin_structures_ONE_ALPHA_DOMAIN.xlsx'
#         )
#
#         # Upload Pdbs
#         call_command('upload_pdbs', fname, stdout=self._out)
#
#         # Get the uploaded Pdb
#         pdb = Pdb.objects.get(pdb="2vdo")
#
#         domains = pdb.alpha_domain.filter(short='bP1')
#
#         # Make sure exactly one domain 'bP1' was added
#         self.assertEqual(
#             domains.count(),
#             1,
#             "Retrieved {0} 'bP1' domains, expected 1".format(domains.count())
#         )
#
#     def test_upload_two_alpha_domain_ok(self):
#         """ Upload a Pdb with two Alpha_domain is OK.
#         """
#
#         fname = prefix_abs_base_path(
#             'test-data/integrin_structures_TWO_ALPHA_DOMAIN.xlsx'
#         )
#
#         # Upload Pdbs
#         call_command('upload_pdbs', fname, stdout=self._out)
#
#         # Get the uploaded Pdb
#         pdb = Pdb.objects.get(pdb="2vdo")
#
#         domains = ['bP1', 'bP2']
#
#         for domain in domains:
#
#             domains = pdb.alpha_domain.filter(short=domain)
#
#             msg = "Retrieved {0} '{1}' domains, expected 1".format(
#                 domains.count(), domains,
#             )
#
#             # Make sure exactly one domain was added
#             self.assertEqual(domains.count(), 1, msg=msg)
#
#     def test_upload_one_other_interactore(self):
#         """ Upload a Pdb with a single Other_interactor is OK.
#         """
#
#         fname = prefix_abs_base_path(
#             'test-data/integrin_structures_ONE_OTHER_INTERACTORS.xlsx'
#         )
#
#         # Upload Pdbs
#         call_command('upload_pdbs', fname, stdout=self._out)
#
#         other_interactors = [
#             "Monoclonal Antibody 10e5 Light Chain",
#         ]
#
#         for other_interactor in other_interactors:
#
#             # Get the uploaded Pdb
#             pdb = Pdb.objects.filter(
#                 pdb="2vdo",
#                 other_interactors__contains=other_interactor,
#             )
#
#             msg = (
#                 "Retrieved {0} '{0}' Pdbs with other interactors, "
#                 "expected 1".format(pdb.count())
#             )
#
#             # Make sure exactly one of each Other_interactor was added
#             self.assertEqual(pdb.count(), 1, msg=msg)
#
#     def test_upload_two_other_interactore(self):
#         """ Upload a Pdb with two Other_interactor is OK.
#         """
#
#         fname = prefix_abs_base_path(
#             'test-data/integrin_structures_TWO_OTHER_INTERACTORS.xlsx'
#         )
#
#         # Upload Pdbs
#         call_command('upload_pdbs', fname, stdout=self._out)
#
#         other_interactors = [
#             "Monoclonal Antibody 10e5 Light Chain",
#             "Monoclonal Antibody 10e5 Heavy Chain",
#         ]
#
#         for other_interactor in other_interactors:
#
#             # Get the uploaded Pdb
#             pdb = Pdb.objects.filter(
#                 pdb="2vdo",
#                 other_interactors__contains=other_interactor,
#             )
#
#             msg = (
#                 "Retrieved {0} '{0}' Pdbs with other interactors, "
#                 "expected 1".format(pdb.count())
#             )
#
#             # Make sure exactly one of each Other_interactor was added
#             self.assertEqual(pdb.count(), 1, msg=msg)
#
#     def test_upload_one_protein_interactor_ok(self):
#         """ Upload a Pdb with a single Protein_interactor is OK.
#         """
#
#         fname = prefix_abs_base_path(
#             'test-data/integrin_structures_ONE_PROTEIN_INTERACTORS.xlsx'
#         )
#
#         # Upload Pdbs
#         call_command('upload_pdbs', fname, stdout=self._out)
#
#         # Get the uploaded Pdb
#         pdb = Pdb.objects.get(pdb="2vdo")
#
#         uniprots = ['P02679']
#
#         for uniprot in uniprots:
#
#             proteins = pdb.protein.filter(uniprot=uniprot)
#
#             msg = (
#                 "Retrieved {0} proteins with uniprot id {0}, "
#                 "expected 1".format(proteins.count(), uniprot)
#             )
#
#             # Make sure exactly one of each Protein_interactor was added
#             self.assertEqual(proteins.count(), 1, msg=msg)
#
#     def test_upload_two_protein_interactor_ok(self):
#         """ Upload a Pdb with two Protein_interactors is OK.
#         """
#
#         fname = prefix_abs_base_path(
#             'test-data/integrin_structures_TWO_PROTEIN_INTERACTORS.xlsx'
#         )
#
#         # Upload Pdbs
#         call_command('upload_pdbs', fname, stdout=self._out)
#
#         # Get the uploaded Pdb
#         pdb = Pdb.objects.get(pdb="2vdo")
#
#         uniprots = ['P02679', 'P12346']
#
#         for uniprot in uniprots:
#
#             proteins = pdb.protein.filter(uniprot=uniprot)
#
#             msg = (
#                 "Retrieved {0} proteins with uniprot id {0}, "
#                 "expected 1".format(proteins.count(), uniprot)
#             )
#
#             # Make sure exactly one of each Protein_interactor was added
#             self.assertEqual(proteins.count(), 1, msg=msg)
#
#
# class DrugParserTest(TestCase):
#     """ Test DrugParser Management Command.
#     """
#
#     def setUp(self):
#         self._out = StringIO()
#
#         # Delete all integrin data
#         call_command('delete_all_integrins', stdout=self._out)
#
#         # Delete all drug data
#         call_command('delete_all_drugs', stdout=self._out)
#
#         # Upload structures shorthands
#         call_command(
#             'upload_structures',
#             prefix_abs_base_path('test-data/domain_shorthands.xlsx'),
#             stdout=self._out,
#         )
#
#         # Upload Monomers
#         call_command(
#             'upload_monomers',
#             prefix_abs_base_path('test-data/integrin_monomers_ok.xlsx'),
#             stdout=self._out,
#         )
#
#         # Upload Dimers
#         call_command(
#             'upload_dimers',
#             prefix_abs_base_path('test-data/integrin_dimers_ok.xlsx'),
#             stdout=self._out,
#         )
#
#     def test_upload_drugs_ok(self):
#         """ Test that we can upload a Drug correctly.
#         """
#
#         # Upload Dimer
#         call_command(
#             'upload_drugs',
#             prefix_abs_base_path('test-data/integrin_drugs_ok.xlsx'),
#             stdout=self._out,
#         )
#
#         # Check that it was added
#         expected = "Added Dimer: alpha-X/beta-2"
#         self.assertIn(
#             expected,
#             self._out.getvalue(),
#             msg="Could not find '{0}' in management output.".format(expected),
#         )
#
#     def test_upload_drugs_two_integrins_ok(self):
#         """ Test that we can upload a Drug with 2 Dimers properly
#         """
#
#         # Create an additional Dimer instance. The default testing Excel sheets
#         # only have 2 monomers and a single Dimer, but we can use the
#         # AlphaFactory and BetaFactory to add an additional Dimer for testing.
#         # The Excel sheet as an extra entry "alpha-A/beta-1"
#         alpha = AlphaFactory.create(name="alpha-A")
#         beta = BetaFactory.create(name="beta-1")
#         DimerFactory.create(alpha=alpha, beta=beta)
#
#         # Upload Dimer
#         call_command(
#             'upload_drugs',
#             prefix_abs_base_path('test-data/integrin_drugs_TWO_DIMERS.xlsx'),
#             stdout=self._out,
#         )
#
#         drugs = Drug.objects.all()
#
#         # Make sure only 1 drug instance was added
#         self.assertEqual(
#             drugs.count(), 1,
#             msg="Expected 1 Drug to be added."
#         )
#
#         self.assertEqual(
#             drugs[0].dimer.count(), 2,
#             msg="Expected 2 Drug.dimer_set.all() instances."
#         )
#
#     def test_upload_missing_Name(self):
#         """ Raise ValidationError when upload a Drug with missing Name.
#         """
#
#         # Expect this in the output
#         expected = (
#             '.*This field cannot be null.*'
#         )
#         fname = prefix_abs_base_path(
#             'test-data/integrin_drugs_MISSING_NAME.xlsx'
#         )
#
#         # Try to upload Monomers
#         with self.assertRaisesRegexp(ValidationError, expected):
#             call_command(
#                 'upload_drugs',
#                 fname,
#                 stdout=self._out,
#             )
#
#     def test_upload_missing_Marketing_name_ok(self):
#         """ Test that we can upload a Drug with a missing Marketing name
#         """
#
#         fname = prefix_abs_base_path(
#             'test-data/integrin_drugs_MISSING_MARKETING_NAME.xlsx'
#         )
#
#         # Try to upload Monomers
#         call_command(
#             'upload_drugs',
#             fname,
#             stdout=self._out,
#         )
#
#     def test_upload_missing_Status(self):
#         """ Raise ValidationError when upload a Drug with missing Status.
#         """
#
#         # Expect this in the output
#         expected = (
#             '.*This field cannot be null.*'
#         )
#         fname = prefix_abs_base_path(
#             'test-data/integrin_drugs_MISSING_STATUS.xlsx'
#         )
#
#         # Try to upload Monomers
#         with self.assertRaisesRegexp(ValidationError, expected):
#             call_command(
#                 'upload_drugs',
#                 fname,
#                 stdout=self._out,
#             )
#
#     def test_upload_missing_Type(self):
#         """ Raise ValidationError when upload a Drug with missing Type.
#         """
#
#         # Expect this in the output
#         expected = (
#             '.*This field cannot be null.*'
#         )
#         fname = prefix_abs_base_path(
#             'test-data/integrin_drugs_MISSING_TYPE.xlsx'
#         )
#
#         # Try to upload Monomers
#         with self.assertRaisesRegexp(ValidationError, expected):
#             call_command(
#                 'upload_drugs',
#                 fname,
#                 stdout=self._out,
#             )
#
#     def test_upload_wrong_Type(self):
#         """ Raise ValidationError when upload a Drug with a wrong Type
#         """
#
#         # Expect this in the output
#         expected = (
#             '.*is not a valid choice.*'
#         )
#         fname = prefix_abs_base_path(
#             'test-data/integrin_drugs_WRONG_TYPE.xlsx'
#         )
#
#         # Try to upload Monomers
#         with self.assertRaisesRegexp(ValidationError, expected):
#             call_command(
#                 'upload_drugs',
#                 fname,
#                 stdout=self._out,
#             )
#
#     def test_upload_missing_Administration(self):
#         """ Raise ValidationError when upload a Drug with missing
#         Administration.
#         """
#
#         # Expect this in the output
#         expected = (
#             '.*This field cannot be null.*'
#         )
#         fname = prefix_abs_base_path(
#             'test-data/integrin_drugs_MISSING_ADMINISTRATION.xlsx'
#         )
#
#         # Try to upload Monomers
#         with self.assertRaisesRegexp(ValidationError, expected):
#             call_command(
#                 'upload_drugs',
#                 fname,
#                 stdout=self._out,
#             )
#
#     def test_upload_missing_ATC_code(self):
#         """ Raise ValidationError when upload a Drug with missing ATC_code.
#         """
#
#         # Expect this in the output
#         expected = (
#             '.*This field cannot be null.*'
#         )
#         fname = prefix_abs_base_path(
#             'test-data/integrin_drugs_MISSING_ATC_CODE.xlsx'
#         )
#
#         # Try to upload Drugs
#         with self.assertRaisesRegexp(ValidationError, expected):
#             call_command(
#                 'upload_drugs',
#                 fname,
#                 stdout=self._out,
#             )
#
#     def test_upload_missing_ATC_definition(self):
#         """ Raise ValidationError when upload a Drug with missing
#         ATC_definition.
#         """
#
#         # Expect this in the output
#         expected = (
#             '.*This field cannot be null.*'
#         )
#         fname = prefix_abs_base_path(
#             'test-data/integrin_drugs_MISSING_ATC_DEFINITION.xlsx'
#         )
#
#         # Try to upload Monomers
#         with self.assertRaisesRegexp(ValidationError, expected):
#             call_command(
#                 'upload_drugs',
#                 fname,
#                 stdout=self._out,
#             )
#
#     def test_upload_missing_Drugbank_ID_ok(self):
#         """ Test that we can upload a Drug with a missing Drugbank_ID
#         """
#
#         fname = prefix_abs_base_path(
#             'test-data/integrin_drugs_MISSING_DRUGBANK_ID.xlsx'
#         )
#
#         # Try to upload Monomers
#         call_command(
#             'upload_drugs',
#             fname,
#             stdout=self._out,
#         )
#
#     def test_upload_missing_Target_integrin(self):
#         """ Raise ValidationError when upload a Drug with missing
#         Target_integrin.
#         """
#
#         # Expect this in the output
#         expected = (
#             '.*cannot be empty.*'
#         )
#         fname = prefix_abs_base_path(
#             'test-data/integrin_drugs_MISSING_TARGET_INTEGRIN.xlsx'
#         )
#
#         # Try to upload Monomers
#         with self.assertRaisesRegexp(ValueError, expected):
#             call_command(
#                 'upload_drugs',
#                 fname,
#                 stdout=self._out,
#             )
#
#     def test_upload_unmatched_Target_integrin(self):
#         """ Raise ValidationError when upload a Drug with an unmatched
#         Target_integrin
#         """
#
#         # Expect this in the output
#         expected = (
#             '.*Dimer matching query does not exist.*'
#         )
#         fname = prefix_abs_base_path(
#             'test-data/integrin_drugs_UNMATCHED_INTEGRIN.xlsx'
#         )
#
#         # Try to upload Monomers
#         with self.assertRaisesRegexp(Dimer.DoesNotExist, expected):
#             call_command(
#                 'upload_drugs',
#                 fname,
#                 stdout=self._out,
#             )
#
#     def test_upload_missing_Launch_year_ok(self):
#         """ Test that we can upload a Drug with a missing Lauch_year
#         """
#
#         fname = prefix_abs_base_path(
#             'test-data/integrin_drugs_MISSING_LAUNCH_YEAR.xlsx'
#         )
#
#         # Try to upload Monomers
#         call_command(
#             'upload_drugs',
#             fname,
#             stdout=self._out,
#         )
#
#     def test_upload_missing_Notes_ok(self):
#         """ Test that we can upload a Drug with a missing Notes
#         """
#
#         fname = prefix_abs_base_path(
#             'test-data/integrin_drugs_MISSING_NOTES.xlsx'
#         )
#
#         # Try to upload Monomers
#         call_command(
#             'upload_drugs',
#             fname,
#             stdout=self._out,
#         )
#
#
# class ProteinInteractoreParserTest(TestCase):
#     """ Test ProteinInteractorParser Management Command.
#     """
#
#     def setUp(self):
#         self._out = StringIO()
#
#         # Delete all integrin data
#         call_command('delete_all_integrins', stdout=self._out)
#
#         # Delete all drug data
#         call_command('delete_all_drugs', stdout=self._out)
#
#         # Upload structures shorthands
#         call_command(
#             'upload_structures',
#             prefix_abs_base_path('test-data/domain_shorthands.xlsx'),
#             stdout=self._out,
#         )
#
#         # Upload Monomers
#         call_command(
#             'upload_monomers',
#             prefix_abs_base_path('test-data/integrin_monomers_ok.xlsx'),
#             stdout=self._out,
#         )
#
#         # Upload Dimers
#         call_command(
#             'upload_dimers',
#             prefix_abs_base_path('test-data/integrin_dimers_ok.xlsx'),
#             stdout=self._out,
#         )
#
#     def test_upload_protein_interactor_ok(self):
#         """ Test that we can upload a ProteinInteractor correctly.
#         """
#
#         fname = prefix_abs_base_path(
#             'test-data/integrin_interactors_ok.xls'
#         )
#
#         # Upload ProteinInteractor
#         call_command(
#             'upload_protein_interactors',
#             fname,
#             stdout=self._out,
#         )
#
#         # Check that it was added
#         expected = "Added DimerToProteinInteractor"
#         self.assertIn(
#             expected,
#             self._out.getvalue(),
#             msg="Could not find '{0}' in management output.".format(expected),
#         )
#
#     def test_upload_protein_interactor_missing_Alternative_names_ok(self):
#         """ Test that we can upload a ProteinInteractor correctly if
#         its missing AlternativeNames.
#         """
#
#         fname = prefix_abs_base_path(
#             'test-data/integrin_interactors_MISSING_ALTERNATIVE_NAMES.xls'
#         )
#         call_command(
#             'upload_protein_interactors',
#             fname,
#             stdout=self._out,
#         )
#
#         # Check that it was added
#         expected = "Added DimerToProteinInteractor"
#         self.assertIn(
#             expected,
#             self._out.getvalue(),
#             msg="Could not find '{0}' in management output.".format(expected),
#         )
#
#     def test_upload_protein_interactor_missing_Function(self):
#         """ Test that we cannot upload a ProteinInteractor if its
#         missing a Function.
#         """
#
#         # Expect this in the output
#         expected = (
#             '.*This field cannot be null.*'
#         )
#
#         fname = prefix_abs_base_path(
#             'test-data/integrin_interactors_MISSING_FUNCTION.xls'
#         )
#
#         with self.assertRaisesRegexp(ValidationError, expected):
#             call_command(
#                 'upload_protein_interactors',
#                 fname,
#                 stdout=self._out
#             )
#
#     def test_upload_protein_interactor_missing_Interaction(self):
#         """ Test that we cannot upload a ProteinInteractor if its
#         missing an Interaction (The boolean column)
#         """
#
#         # Expect this in the output.
#         # For some reason BooleanFields raise IntegrityErrors
#         expected = (
#             '.*NOT NULL constraint failed.*'
#         )
#
#         fname = prefix_abs_base_path(
#             'test-data/integrin_interactors_MISSING_INTERACTION.xls'
#         )
#
#         # For some reason BooleanFields raise IntegrityErrors
#         with self.assertRaisesRegexp(IntegrityError, expected):
#             call_command(
#                 'upload_protein_interactors',
#                 fname,
#                 stdout=self._out
#             )
#
#     def test_upload_protein_interactor_missing_Annotated(self):
#         """ Test that we cannot upload a ProteinInteractor if its
#         missing a the Annotated value (a boolean column)
#         """
#
#         # Expect this in the output.
#         # For some reason BooleanFields raise IntegrityErrors
#         expected = (
#             '.*NOT NULL constraint failed.*'
#         )
#
#         fname = prefix_abs_base_path(
#             'test-data/integrin_interactors_MISSING_ANNOTATED.xls'
#         )
#
#         # For some reason BooleanFields raise IntegrityErrors
#         with self.assertRaisesRegexp(IntegrityError, expected):
#             call_command(
#                 'upload_protein_interactors',
#                 fname,
#                 stdout=self._out
#             )
#
#     def test_upload_protein_interactor_missing_Motif_type(self):
#         """ Test that we cannot upload a ProteinInteractor if its
#         missing a Motif_type
#         """
#
#         # Expect this in the output
#         expected = (
#             '.*This field cannot be null.*'
#         )
#
#         fname = prefix_abs_base_path(
#             'test-data/integrin_interactors_MISSING_MOTIF_TYPE.xls'
#         )
#
#         with self.assertRaisesRegexp(ValidationError, expected):
#             call_command(
#                 'upload_protein_interactors',
#                 fname,
#                 stdout=self._out
#             )
#
#     def test_upload_protein_interactor_missing_Organism(self):
#         """ Test that we cannot upload a ProteinInteractor if it
#         missing an Organism
#         """
#
#         # Expect this in the output
#         expected = (
#             '.*This field cannot be null.*'
#         )
#
#         fname = prefix_abs_base_path(
#             'test-data/integrin_interactors_MISSING_ORGANISM.xls'
#         )
#
#         with self.assertRaisesRegexp(ValidationError, expected):
#             call_command(
#                 'upload_protein_interactors',
#                 fname,
#                 stdout=self._out
#             )
#
#     def test_upload_protein_interactor_missing_Protein_name(self):
#         """ Test that we cannot upload a ProteinInteractor if it
#         missing a Protein name
#         """
#
#         # Expect this in the output
#         expected = (
#             ".*'name' cannot be None/empty.*"
#         )
#
#         fname = prefix_abs_base_path(
#             'test-data/integrin_interactors_MISSING_PROTEIN_NAME.xls'
#         )
#
#         with self.assertRaisesRegexp(ValueError, expected):
#             call_command(
#                 'upload_protein_interactors',
#                 fname,
#                 stdout=self._out
#             )
#
#     def test_upload_protein_interactor_missing_Site_boundaries(self):
#         """ Test that we cannot upload a ProteinInteractor if it
#         missing Site_boundaries
#         """
#
#         # Expect this in the output
#         expected = (
#             '.*Could not parse start-stop.*'
#         )
#
#         fname = prefix_abs_base_path(
#             'test-data/integrin_interactors_MISSING_SITE_BOUNDARIES.xls'
#         )
#
#         with self.assertRaisesRegexp(Exception, expected):
#             call_command(
#                 'upload_protein_interactors',
#                 fname,
#                 stdout=self._out
#             )
#
#             'upload_protein_interactors',
#
#     def test_upload_protein_interactor_missing_Site_definition(self):
#         """ Test that we cannot upload a ProteinInteractor if it
#         missing Site_definition
#         """
#
#         # Expect this in the output
#         expected = (
#             '.*This field cannot be null.*'
#         )
#
#         fname = prefix_abs_base_path(
#             'test-data/integrin_interactors_MISSING_SITE_DEFINITION.xls'
#         )
#
#         with self.assertRaisesRegexp(ValidationError, expected):
#             call_command(
#                 'upload_protein_interactors',
#                 fname,
#                 stdout=self._out
#             )
#
#             'upload_protein_interactors',
#
#     def test_upload_protein_interactor_missing_Structural_state(self):
#         """ Test that we cannot upload a ProteinInteractor if it
#         missing Structural_state
#         """
#
#         # Expect this in the output
#         expected = (
#             '.*This field cannot be null.*'
#         )
#
#         fname = prefix_abs_base_path(
#             'test-data/integrin_interactors_MISSING_STRUCTURAL_STATE.xls'
#         )
#
#         with self.assertRaisesRegexp(ValidationError, expected):
#             call_command(
#                 'upload_protein_interactors',
#                 fname,
#                 stdout=self._out
#             )
#
#     def test_upload_protein_interactor_missing_Taxonomic_group(self):
#         """ Test that we cannot upload a ProteinInteractor if it
#         missing Taxonomic_group
#         """
#
#         # Expect this in the output
#         expected = (
#             '.*This field cannot be null.*'
#         )
#
#         fname = prefix_abs_base_path(
#             'test-data/integrin_interactors_MISSING_TAXONOMIC_GROUP.xls'
#         )
#
#         with self.assertRaisesRegexp(ValidationError, expected):
#             call_command(
#                 'upload_protein_interactors',
#                 fname,
#                 stdout=self._out
#             )
#
#             'upload_protein_interactors',
#
#     def test_upload_protein_interactor_missing_Uniprot_accession(self):
#         """ Test that we cannot upload a ProteinInteractor if it
#         missing a Uniprot_accession
#         """
#
#         # Expect this in the output
#         expected = (
#             '.*This field cannot be null.*'
#         )
#
#         fname = prefix_abs_base_path(
#             'test-data/integrin_interactors_MISSING_UNIPROT_ACCESSION.xls'
#         )
#
#         with self.assertRaisesRegexp(ValidationError, expected):
#             call_command(
#                 'upload_protein_interactors',
#                 fname,
#                 stdout=self._out
#             )
#
#             'upload_protein_interactors',
#
#     def test_upload_unmatched_Dimer(self):
#         """ Raise ValidationError when upload a ProteinInteractor with
#         an unmatched Dimer
#         """
#
#         # Expect this in the output
#         expected = (
#             '.*Dimer matching query does not exist.*'
#         )
#         fname = prefix_abs_base_path(
#             'test-data/integrin_interactors_UNMATCHED_DIMER.xls'
#         )
#
#         # Try to upload Monomers
#         with self.assertRaisesRegexp(Dimer.DoesNotExist, expected):
#             call_command(
#                 'upload_protein_interactors',
#                 fname,
#                 stdout=self._out,
#             )
#
#
#     def test_upload_protein_interactor_missing_Ref(self):
#         """ Test that we cannot upload a ProteinInteractor if it
#         is missing the Ref(everence)
#         """
#
#         # Expect this in the output
#         expected = (
#             '.*This field cannot be null.*'
#         )
#
#         fname = prefix_abs_base_path(
#             'test-data/integrin_interactors_MISSING_REF.xls'
#         )
#
#         with self.assertRaisesRegexp(ValidationError, expected):
#             call_command(
#                 'upload_protein_interactors',
#                 fname,
#                 stdout=self._out
#             )
#
#     def test_upload_protein_interactor_missing_Structures_ok(self):
#         """ Test that we can upload a ProteinInteractor correctly if
#         Structures are missing
#         """
#
#         fname = prefix_abs_base_path(
#             'test-data/integrin_interactors_MISSING_STRUCTURES.xls'
#         )
#
#         # Upload ProteinInteractor
#         call_command(
#             'upload_protein_interactors',
#             fname,
#             stdout=self._out,
#         )
#
#         # Check that it was added
#         expected = "Added DimerToProteinInteractor"
#         self.assertIn(
#             expected,
#             self._out.getvalue(),
#             msg="Could not find '{0}' in management output.".format(expected),
#         )
#
#     def test_upload_protein_interactor_no_interactions_ok(self):
#         """ Test that we can upload a ProteinInteractor correctly if it has
#         not interactions
#         """
#
#         fname = prefix_abs_base_path(
#             'test-data/integrin_interactors_NO_INTERACTIONS.xls'
#         )
#
#         # Upload ProteinInteractor
#         call_command(
#             'upload_protein_interactors',
#             fname,
#             stdout=self._out,
#         )
#
#         # Check that it was added
#         expected = "Added ProteinInteractor"
#         self.assertIn(
#             expected,
#             self._out.getvalue(),
#             msg="Could not find '{0}' in management output.".format(expected),
#         )
#
#         # Check that no DimerToProteinInteractor was added
#         expected = "Added DimerToProteinInteractor"
#         self.assertNotIn(
#             expected,
#             self._out.getvalue(),
#             msg="Found '{0}' in management output.".format(expected),
#         )
#
#
#     def test_upload_protein_interactor_two_alterantive_names_ok(self):
#         """ Test that we can upload a ProteinInteractor correctly if it has
#         two Alternative_names, and that the names are uploaded correctly.
#         """
#
#         fname = prefix_abs_base_path(
#             'test-data/integrin_interactors_TWO_ALTERNATIVE_NAMES.xls'
#         )
#
#         # Upload ProteinInteractor
#         call_command(
#             'upload_protein_interactors',
#             fname,
#             stdout=self._out,
#         )
#
#         # Check that it was added
#         expected = "Added DimerToProteinInteractor"
#         self.assertIn(
#             expected,
#             self._out.getvalue(),
#             msg="Could not find '{0}' in management output.".format(expected),
#         )
#
#         # Check that the two names were added correctly
#         expected_names = [
#             "Phosphatidylcholine 2-acylhydrolase",
#             "Some other name",
#         ]
#
#         for expected_name in expected_names:
#
#             alternative_names = AlternativeName.objects.filter(
#                 name=expected_name,
#                 protein__uniprot='B5U6Z2',
#             )
#
#             self.assertEqual(
#                 alternative_names.count(),
#                 1,
#                 "Retrieved {0} uploaded AlternativeNames, expected 1".format(
#                     alternative_names.count()
#                 ),
#             )
#
#     def test_upload_protein_interactor_missing_val_ok(self):
#         """ Test that we can upload a ProteinInteractor correctly if it is
#         missing a val(ue)
#         """
#
#         fname = prefix_abs_base_path(
#             'test-data/integrin_interactors_MISSING_VALUE.xls'
#         )
#
#         # Upload ProteinInteractor
#         call_command(
#             'upload_protein_interactors',
#             fname,
#             stdout=self._out,
#         )
#
#         # Check that it was added
#         expected = "Added DimerToProteinInteractor"
#         self.assertIn(
#             expected,
#             self._out.getvalue(),
#             msg="Could not find '{0}' in management output.".format(expected),
#         )
