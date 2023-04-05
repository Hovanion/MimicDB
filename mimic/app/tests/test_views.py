# import os
# import re
#
# from django.test import TestCase
# from django.urls import reverse
# from django.conf import settings
#
# from app.models import Monomer
# from app.models import Dimer
# from app.models import Drug
#
# from app.tests.factories import AlphaFactory
# from app.tests.factories import BetaFactory
# from app.tests.factories import AlternativeNameFactory
# from app.tests.factories import DimerFactory
# from app.tests.factories import PdbFactory
# from app.tests.factories import DrugFactory
# from app.tests.factories import DimerToDrugFactory
# from app.tests.factories import ProteinInteractorFactory
# from app.tests.factories import DimerToProteinInteractorFactory
# from app.tests.factories import PdbToProteinFactory
# ProteinInteractorFactory
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
# class MonomerViewTest(TestCase):
#     """ Test the Monomer view.
#     """
#
#     def setUp(self):
#         Monomer.objects.all().delete()
#         Dimer.objects.all().delete()
#
#     def test_monomer_alpha_view_200(self):
#         """ Test that the Alpha monomers view returns 200.
#         """
#
#         alpha = AlphaFactory.create()
#
#         response = self.client.get(
#             reverse('alpha', args=(alpha.name,)),
#         )
#         self.assertEqual(response.status_code, 200)
#
#     def test_monomer_beta_view_200(self):
#         """ Test that the Beta monomers view returns 200.
#         """
#
#         beta = BetaFactory.create()
#
#         response = self.client.get(
#             reverse('beta', args=(beta.name,)),
#         )
#         self.assertEqual(response.status_code, 200)
#
#     def test_monomer_alpha_view_404_not_exist(self):
#         """ Test that the Alpha monomers view returns 404 if monomer
#         does not exist.
#         """
#
#         AlphaFactory.create_batch(10)
#
#         response = self.client.get(
#             reverse('alpha', args=("Alpha-Not",)),
#         )
#         self.assertEqual(response.status_code, 404)
#
#     def test_monomer_beta_view_404_not_exist(self):
#         """ Test that the Beta monomers view returns 404 if monomer does
#         not exist.
#         """
#
#         BetaFactory.create_batch(10)
#
#         response = self.client.get(
#             reverse('beta', args=("Beta-Not",)),
#         )
#         self.assertEqual(response.status_code, 404)
#
#     def test_monomer_alpha_view_404_beta_name(self):
#         """ Test that the Alpha monomers view returns 404 if a Beta
#         monomer is specified.
#         """
#
#         alpha = AlphaFactory.create()
#         BetaFactory.create_batch(10)
#
#         response = self.client.get(
#             reverse('beta', args=(alpha.name,)),
#         )
#         self.assertEqual(response.status_code, 404)
#
#     def test_monomer_beta_view_404_alpha_name(self):
#         """ Test that the Beta monomers view returns 404 if an Alpha
#         monomer is specified.
#         """
#
#         AlphaFactory.create_batch(10)
#         beta = BetaFactory.create()
#
#         response = self.client.get(
#             reverse('alpha', args=(beta.name,)),
#         )
#         self.assertEqual(response.status_code, 404)
#
#     def test_monomer_alternative_names(self):
#         """ Test that the Monomer's alternative names are shown.
#         """
#
#         alpha = AlphaFactory.create()
#         alterantive_name = AlternativeNameFactory.create()
#         alpha.protein.alternativename_set.add(alterantive_name)
#
#         response = self.client.get(
#             reverse('alpha', args=(alpha.name,)),
#         )
#         self.assertContains(
#             response, alterantive_name.name,
#             msg_prefix="Could not find AlternativeName on template",
#         )
#
#     def test_monomer_alternative_name_none(self):
#         """ Test that "(none)" is shown if Monomer's has no alternative names.
#         """
#
#         alpha = AlphaFactory.create()
#
#         response = self.client.get(
#             reverse('alpha', args=(alpha.name,)),
#         )
#         self.assertContains(
#             response, "(none)",
#             msg_prefix="Could not find string '(none)' on template",
#         )
#
#     def test_monomer_alpha_interaction_domain_hidden(self):
#         """ Test that the 'alpha interaction domain' field is not displayed for
#         Beta subunits
#         """
#
#         alpha = BetaFactory.create(
#             alpha_interaction_domain=None,
#         )
#
#         response = self.client.get(
#             reverse('beta', args=(alpha.name,)),
#         )
#
#         expected = "Inserted interaction domain present"
#
#         self.assertNotContains(
#             response, expected,
#             msg_prefix="Found incorrect string '{0}' on template".format(
#                 expected,
#             ),
#         )
#
#     def test_monomer_alpha_interaction_domain_yes(self):
#         """ Test that the 'Alpha interaction domain' field and the string 'yes'
#         is display if alpha_interaction_domain == True
#         """
#
#         alpha = AlphaFactory.create(
#             alpha_interaction_domain=True,
#         )
#
#         response = self.client.get(
#             reverse('alpha', args=(alpha.name,)),
#         )
#
#         expected = "Inserted interaction domain present"
#
#         self.assertContains(
#             response, expected,
#             msg_prefix="Could not find string '{0}' on template".format(
#                 expected,
#             ),
#         )
#
#         expected = "yes"
#
#         self.assertContains(
#             response, expected,
#             msg_prefix="Could not find string '{0}' on template".format(
#                 expected,
#             ),
#         )
#
#
#
#
#
# class DimerViewTest(TestCase):
#     """ Test the Dimer view.
#     """
#
#     def setUp(self):
#         Monomer.objects.all().delete()
#         Dimer.objects.all().delete()
#
#     def test_dimer_view_200(self):
#         """ Test that the Dimer view returns 200.
#         """
#
#         dimer = DimerFactory.create()
#
#         response = self.client.get(
#             reverse('dimer', args=(dimer.lookup_name,)),
#         )
#         self.assertEqual(response.status_code, 200)
#
#     def test_dimer_view_404(self):
#         """ Test that the Dimer view returns 404 if dimer does not exist.
#         """
#
#         DimerFactory.create_batch(3)
#
#         response = self.client.get(
#             reverse('dimer', args=("alpha-None_beta-None",)),
#         )
#         self.assertEqual(response.status_code, 404)
#
#     def test_dimer_view_drugs_one(self):
#         """ Dimer with 1 drug: show drug name.
#         """
#
#         dimer_to_drug = DimerToDrugFactory.create()
#         dimer = dimer_to_drug.dimer
#         drug = dimer_to_drug.drug
#
#         response = self.client.get(
#             reverse('dimer', args=(dimer.lookup_name,)),
#         )
#
#         self.assertContains(response, drug.name)
#
#     def test_dimer_view_drugs_one_no_comma(self):
#         """ Dimer with 1 drug: show drug name, without commas.
#         """
#
#         dimer_to_drug = DimerToDrugFactory.create()
#         dimer = dimer_to_drug.dimer
#         drug = dimer_to_drug.drug
#
#         response = self.client.get(
#             reverse('dimer', args=(dimer.lookup_name,)),
#         )
#
#         expected = re.compile(".*{0}\S+[^,].*".format(drug.name))
#         found = expected.findall(response.content.decode('utf-8'))
#
#         msg = (
#             "Expected find a link similar to "
#             "'{0}' (without comma)".format(drug.name)
#             )
#         self.assertEqual(len(found), 1, msg=msg)
#
#     def test_dimer_view_protein_interactor_one(self):
#         """ Dimer with 1 protein interactor: show protein interactor name.
#         """
#
#         d2pi = DimerToProteinInteractorFactory.create()
#
#         response = self.client.get(
#             reverse('dimer', args=(d2pi.dimer.lookup_name,)),
#         )
#
#         self.assertContains(response, d2pi.protein_interactor.name)
#
#     def test_dimer_view_protein_interactor_two(self):
#         """ Dimer with 2 protein interactor: show both protein interactor name.
#         """
#
#         d2pi_1 = DimerToProteinInteractorFactory.create()
#         d2pi_2 = DimerToProteinInteractorFactory.create(
#                 dimer=d2pi_1.dimer,
#                 )
#
#         response = self.client.get(
#             reverse('dimer', args=(d2pi_1.dimer.lookup_name,)),
#         )
#
#         self.assertContains(response, d2pi_1.protein_interactor.name)
#         self.assertContains(response, d2pi_2.protein_interactor.name)
#
#     def test_dimer_view_protein_interactor_native(self):
#         """ Dimer with 1 human protein interactor: show 'native' on template
#         """
#
#         protein_interactor = ProteinInteractorFactory.create(
#             taxonomic_group="Human",
#         )
#         d2pi = DimerToProteinInteractorFactory.create(
#             protein_interactor=protein_interactor,
#         )
#
#         response = self.client.get(
#             reverse('dimer', args=(d2pi.dimer.lookup_name,)),
#         )
#
#         self.assertContains(response, 'native')
#
#     def test_dimer_view_protein_interactor_non_native(self):
#         """ Dimer with 1 non-human protein interactor: show 'non-native' and
#         taxonomic_group on template.
#         """
#
#         taxonomic_group = "Snakes!"
#
#         protein_interactor = ProteinInteractorFactory.create(
#             taxonomic_group=taxonomic_group
#         )
#         d2pi = DimerToProteinInteractorFactory.create(
#             protein_interactor=protein_interactor,
#         )
#
#         response = self.client.get(
#             reverse('dimer', args=(d2pi.dimer.lookup_name,)),
#         )
#
#         self.assertContains(response, 'non-native')
#         self.assertContains(response, taxonomic_group)
#
#
# class DrugViewTest(TestCase):
#     """ Test the Drug view.
#     """
#
#     def setUp(self):
#         Monomer.objects.all().delete()
#         Dimer.objects.all().delete()
#         Drug.objects.all().delete()
#
#     def test_drug_view_200(self):
#         """ Test that the Drug view returns 200.
#         """
#
#         drug = DrugFactory.create()
#
#         response = self.client.get(
#             reverse('drug', args=(drug.name,)),
#         )
#         self.assertEqual(response.status_code, 200)
#
#     def test_drug_view_404(self):
#         """ Test that the Drug view returns 404 if drug does not exist.
#         """
#
#         DrugFactory.create_batch(3)
#
#         response = self.client.get(
#             reverse('drug', args=("NotADrug",)),
#         )
#         self.assertEqual(response.status_code, 404)
#
#     def test_launch_year_none(self):
#         """ Test that the Drug view shows "(none)" if for Launch year if
#         Drug does not have one.
#         """
#
#         drug = DrugFactory.create(launch_year=None)
#
#         response = self.client.get(
#             reverse('drug', args=(drug.name,)),
#         )
#
#         # Expect this string in the rendered template
#         expected = "(none)"
#
#         self.assertContains(response, expected, count=1)
#
#     def test_launch_year(self):
#         """ Test that the Drug view shows the Launch year if the Drug has
#         one.
#         """
#
#         LAUNCH_YEAR = "1999"
#
#         drug = DrugFactory.create(launch_year=LAUNCH_YEAR)
#
#         response = self.client.get(
#             reverse('drug', args=(drug.name,)),
#         )
#
#         self.assertContains(response, LAUNCH_YEAR, count=1)
#
#     def test_drugbank_none(self):
#         """ Test that the Drug view shows "(none)" if for Drugbank link if the
#         Drug does not have one.
#         """
#
#         drug = DrugFactory.create(drugbank=None)
#
#         response = self.client.get(
#             reverse('drug', args=(drug.name,)),
#         )
#
#         # Expect this string in the rendered template
#         expected = "(none)"
#
#         self.assertContains(response, expected, count=1)
#
#     def test_drugbank(self):
#         """ Test that the Drug view shows the drugbank link if the Drug has
#         one.
#         """
#
#         drug = DrugFactory.create()
#
#         response = self.client.get(
#             reverse('drug', args=(drug.name,)),
#         )
#
#         # Expect this string in the rendered template
#         expected = drug.drugbank_link()
#
#         self.assertContains(response, expected, count=1)
#
#     def test_marketing_name_none(self):
#         """ Test that the Drug view shows "(none)" if for Marketing Name if
#         Drug does not have one.
#         """
#
#         drug = DrugFactory.create(marketing_name=None)
#
#         response = self.client.get(
#             reverse('drug', args=(drug.name,)),
#         )
#
#         # Expect this string in the rendered template
#         expected = "(none)"
#
#         self.assertContains(response, expected, count=1)
#
#     def test_marketing_name(self):
#         """ Test that the Drug view shows the marketing name if the Drug has
#         one.
#         """
#
#         MARKETING_NAME = "Banjo"
#
#         drug = DrugFactory.create(marketing_name=MARKETING_NAME)
#
#         response = self.client.get(
#             reverse('drug', args=(drug.name,)),
#         )
#
#         self.assertContains(response, MARKETING_NAME, count=1)
#
#     def test_notes_none(self):
#         """ Test that the Drug view shows "(none)" if for notes if Drug does
#         not have one.
#         """
#
#         drug = DrugFactory.create(notes=None)
#
#         response = self.client.get(
#             reverse('drug', args=(drug.name,)),
#         )
#
#         # Expect this string in the rendered template
#         expected = "(none)"
#
#         self.assertContains(response, expected, count=1)
#
#     def test_notes(self):
#         """ Test that the Drug view shows the notes if the Drug has one.
#         """
#
#         NOTES = """It was a dark and stormy night; the rain fell in torrents —
#         except at occasional intervals, when it was checked by a violent gust
#         of wind which swept up the streets (for it is in London that our scene
#         lies), rattling along the housetops, and fiercely agitating the scanty
#         flame of the lamps that struggled against the darkness."""
#
#         drug = DrugFactory.create(notes=NOTES)
#
#         response = self.client.get(
#             reverse('drug', args=(drug.name,)),
#         )
#
#         self.assertContains(response, NOTES, count=1)
#
#     def test_dimers(self):
#         """ Test that the Drug view shows the Dimer objects with a ForeignKey
#         to the drug.
#         """
#
#         dimer_to_drug = DimerToDrugFactory.create()
#
#         response = self.client.get(
#             reverse('drug', args=(dimer_to_drug.drug.name,)),
#         )
#
#         self.assertContains(response, dimer_to_drug.dimer.display_name(), count=1)
#
#
# class DrugListViewTest(TestCase):
#     """ Test DrugListView
#     """
#
#     def test_drugs_list_view_200(self):
#         """ Test that the DrugListView returns 200
#         """
#
#         response = self.client.get(
#             reverse('drugs')
#         )
#         self.assertEqual(response.status_code, 200)
#
#     def test_drugbank_link(self):
#         """ Test that the DrugListView has links to drugbank
#         """
#
#         drugs = DrugFactory.create_batch(20)
#
#         response = self.client.get(
#             reverse('drugs')
#         )
#
#         for drug in drugs:
#             expected = "https://www.drugbank.ca/drugs/{0}".format(
#                 drug.drugbank,
#             )
#
#             self.assertContains(
#                 response, expected,
#                 msg_prefix="Did not find Drugnbank link'{0}'".format(
#                     expected
#                 )
#             )
#
#     def test_proteininteraction_list_contents_200(self):
#         """ Test that the ProteinInteractionListView shows all ProteinInteractions
#         """
#
#         drugs = DrugFactory.create_batch(10)
#
#         # Add a dimer object
#         for drug in drugs:
#             dimer_to_drug = DimerToDrugFactory.create()
#             drug.dimertodrug_set.add(dimer_to_drug)
#             drug.save()
#
#         response = self.client.get(
#             reverse('drugs')
#         )
#
#         for drug in drugs:
#
#             self.assertContains(
#                 response, drug.name,
#                 msg_prefix="Did not find name '{0}'".format(
#                     drug.name
#                 )
#             )
#             self.assertContains(
#                 response, drug.drugbank,
#                 msg_prefix="Did not find drugbank '{0}'".format(
#                     drug.drugbank
#                 )
#             )
#             self.assertContains(
#                 response, drug.marketing_name,
#                 msg_prefix="Did not find marketing name '{0}'".format(
#                     drug.marketing_name
#                 )
#             )
#             self.assertContains(
#                 response, drug.launch_year,
#                 msg_prefix="Did not find launch year '{0}'".format(
#                     drug.launch_year
#                 )
#             )
#             self.assertContains(
#                 response, drug.drug_type,
#                 msg_prefix="Did not find drug type '{0}'".format(
#                     drug.drug_type
#                 )
#             )
#             for dimer in drug.dimer.all():
#                 self.assertContains(
#                     response, dimer.display_name(),
#                     msg_prefix="Did not find dimer name '{0}'".format(
#                         dimer.display_name()
#                     )
#                 )
#
#
# class HomeUrlsTest(TestCase):
#     """ Test home page urls
#     """
#
#     def setUp(self):
#         Monomer.objects.all().delete()
#         Dimer.objects.all().delete()
#
#     def test_home_url_200(self):
#         """ Test that the Home view returns 200.
#         """
#
#         # Create a single dimer object (to shown on the homepage)
#         # This one must be one of the selected examples in
#         # views.RANDOM_EXAMPLE_DIMERS
#         DimerFactory.create(
#             alpha__name='alpha-1',
#             beta__name='beta-1',
#         )
#
#         response = self.client.get(
#             reverse('home')
#         )
#         self.assertEqual(response.status_code, 200)
#
#     def test_base_url_redirect(self):
#         """ Make sure base URL redirects to home
#         """
#
#         # Create a single dimer object (to shown on the homepage)
#         # This one must be one of the selected examples in
#         # views.RANDOM_EXAMPLE_DIMERS
#         DimerFactory.create(
#             alpha__name='alpha-1',
#             beta__name='beta-1',
#         )
#
#         response = self.client.get('')
#         self.assertRedirects(response, reverse('home'), 301)
#
#     def test_base_app_url_redirect(self):
#         """ Make sure base URL for 'app' app redirects to home
#         """
#         # Create a single dimer object (to shown on the homepage)
#         # This one must be one of the selected examples in
#         # views.RANDOM_EXAMPLE_DIMERS
#         DimerFactory.create(
#             alpha__name='alpha-1',
#             beta__name='beta-1',
#         )
#
#
#         response = self.client.get(reverse('app'))
#         self.assertRedirects(response, reverse('home'), 301)
#
#
# class AboutUrlsTest(TestCase):
#     """ Test about page urls
#     """
#
#     def test_about_url_200(self):
#         """ Test that the Home view returns 200.
#         """
#
#         response = self.client.get(
#             reverse('about')
#         )
#         self.assertEqual(response.status_code, 200)
#
#
# class PdbListViewTest(TestCase):
#     """ Test Pdb list view
#     """
#
#     def test_pdb_list_view_200(self):
#         """ Test that the PdbListView returns 200
#         """
#
#         response = self.client.get(
#             reverse('pdbs')
#         )
#         self.assertEqual(response.status_code, 200)
#
#     def test_pdb_list_contents_200(self):
#         """ Test that the PdbListView shows all Pdbs
#         """
#
#         pdbs = PdbFactory.create_batch(20)
#
#         response = self.client.get(
#             reverse('pdbs')
#         )
#
#         for pdb in pdbs:
#             self.assertContains(
#                 response, pdb.pdb,
#                 msg_prefix="Did not find Pdb '{0}'".format(pdb.pdb)
#             )
#             self.assertContains(
#                 response, pdb.alpha.name,
#                 msg_prefix="Did not find Alpha '{0}'".format(pdb.alpha.name)
#             )
#             self.assertContains(
#                 response, pdb.beta.name,
#                 msg_prefix="Did not find Beta '{0}'".format(pdb.beta.name)
#             )
#
#     def test_pdb_protein_interactors_no(self):
#         """ Test "Protein interactors" shows 'no' if there are none
#         """
#
#         PdbFactory.create()
#
#         response = self.client.get(
#             reverse('pdbs')
#         )
#
#         expected = "<td>—</td>"
#         self.assertContains(response, expected, html=True)
#
#     def test_pdb_protein_interactors_one_yes(self):
#         """ Test "Protein interactors" shows 'yes' if there is one
#         """
#
#         pdb = PdbFactory.create()
#
#         PdbToProteinFactory.create(pdb=pdb)
#
#         response = self.client.get(
#             reverse('pdbs')
#         )
#
#         expected = "<td>✔</td>"
#         self.assertContains(response, expected, html=True)
#
#     def test_pdb_protein_interactors_two_yes(self):
#         """ Test "Protein interactors" shows 'yes' if there is two
#         """
#
#         pdb = PdbFactory.create()
#
#         PdbToProteinFactory.create(pdb=pdb)
#         PdbToProteinFactory.create(pdb=pdb)
#
#         response = self.client.get(
#             reverse('pdbs')
#         )
#
#         expected = "<td>✔</td>"
#         self.assertContains(response, expected, html=True)
#
#     def test_pdb_other_interactors_no(self):
#         """ Test "Other interactors" shows 'no' if there are none
#         """
#
#         PdbFactory.create(other_interactors=None)
#
#         response = self.client.get(
#             reverse('pdbs')
#         )
#
#         expected = "<td>—</td>"
#         self.assertContains(response, expected, html=True)
#
#     def test_pdb_other_interactors_yes(self):
#         """ Test "Other interactors" shows 'yes' if there is one
#         """
#
#         PdbFactory.create(other_interactors="something")
#
#         response = self.client.get(
#             reverse('pdbs')
#         )
#
#         expected = '<span class="true">✔</span>'
#         self.assertContains(response, expected, html=True)
#
#
# class DimerListViewTest(TestCase):
#     """ Test Dimer list view
#     """
#
#     def test_dimer_list_view_200(self):
#         """ Test that the DimerListView returns 200
#         """
#
#         response = self.client.get(
#             reverse('integrins')
#         )
#         self.assertEqual(response.status_code, 200)
#
#     def test_dimer_list_contents_200(self):
#         """ Test that the DimerListView shows all Dimers
#         """
#
#         dimers = DimerFactory.create_batch(10)
#
#         response = self.client.get(
#             reverse('integrins')
#         )
#
#         for dimer in dimers:
#             self.assertContains(
#                 response, dimer.display_name(),
#                 msg_prefix="Did not find Dimer '{0}'".format(dimer.display_name())
#             )
#             self.assertContains(
#                 response, dimer.alpha.name,
#                 msg_prefix="Did not find Alpha '{0}'".format(dimer.alpha.name)
#             )
#             self.assertContains(
#                 response, dimer.beta.name,
#                 msg_prefix="Did not find Beta '{0}'".format(dimer.beta.name)
#             )
#
#
#
#         self.assertEqual(response.status_code, 200)
#
#
# class DimerToDrugListViewTest(TestCase):
#     """ Test DimerToDrug list view
#     """
#
#     def test_dimer_to_drug_list_view_200(self):
#         """ Test that the DimerToDrugListView returns 200
#         """
#
#         response = self.client.get(
#             reverse('drugs')
#         )
#         self.assertEqual(response.status_code, 200)
#
#     def test_dimer_list_contents_200(self):
#         """ Test that the DimerListView shows all Dimers
#         """
#
#         dimer_to_drugs = DimerToDrugFactory.create_batch(10)
#
#         response = self.client.get(
#             reverse('drugs')
#         )
#
#         for dimer_to_drug in dimer_to_drugs:
#             self.assertContains(
#                 response, dimer_to_drug.dimer.display_name(),
#                 msg_prefix="Did not find Dimer '{0}'".format(
#                     dimer_to_drug.dimer.display_name(),
#                 )
#             )
#             self.assertContains(
#                 response, dimer_to_drug.drug.name,
#                 msg_prefix="Did not find Drug '{0}'".format(
#                     dimer_to_drug.drug.name,
#                 )
#             )
#
#         self.assertEqual(response.status_code, 200)
#
#
# class ProteinInteractorViewTest(TestCase):
#     """ Test the ProteinInteractorViewTest DetailView.
#     """
#
#     def setUp(self):
#         Monomer.objects.all().delete()
#         Dimer.objects.all().delete()
#
#     def test_protein_interactor_view_200(self):
#         """ Test that the ProteinInteractorDetialView view returns 200.
#         """
#
#         protein_interactor = ProteinInteractorFactory.create()
#
#         response = self.client.get(
#             reverse(
#                 'protein-interactor',
#                 args=(protein_interactor.protein.uniprot,)),
#         )
#         self.assertEqual(response.status_code, 200)
#
#     def test_protein_interactor_view_404(self):
#         """ Test that the ProteinInteractorDetialView view returns 404 is the
#         ProteinInteractor does not exist.
#         """
#
#         ProteinInteractorFactory.create_batch(3)
#
#         response = self.client.get(
#             reverse(
#                 'protein-interactor',
#                 args=("NotAProteinInteractor",)),
#         )
#         self.assertEqual(response.status_code, 404)
#
#     def test_affinity(self):
#         """ Test that the ProteinInteractor view shows the affinity if it has one
#         one.
#         """
#
#         AFFINITY = "AFFINITY"
#
#         protein_interactor = ProteinInteractorFactory.create(
#             annotated=True,
#         )
#         DimerToProteinInteractorFactory.create(
#             protein_interactor=protein_interactor,
#             affinity=AFFINITY,
#         )
#
#         response = self.client.get(
#             reverse(
#                 'protein-interactor',
#                 args=(protein_interactor.protein.uniprot,)),
#         )
#
#         self.assertContains(response, AFFINITY, count=1)
#
#     def test_affinity_na(self):
#         """ Test that the ProteinInteractor view shows 'N/A' if the
#         affinity = None.
#         """
#
#         protein_interactor = ProteinInteractorFactory.create(
#             annotated=True,
#         )
#         DimerToProteinInteractorFactory.create(
#             protein_interactor=protein_interactor,
#             affinity=None,
#         )
#
#         response = self.client.get(
#             reverse(
#                 'protein-interactor',
#                 args=(protein_interactor.protein.uniprot,)),
#         )
#
#         self.assertContains(response, "N/A", count=1)
#
#     def test_pmids_one(self):
#         """ Test that the ProteinInteractor view shows one PMID link correctly.
#         """
#
#         PMID = "12345"
#
#         protein_interactor = ProteinInteractorFactory.create(
#             annotated=True,
#         )
#         DimerToProteinInteractorFactory.create(
#             protein_interactor=protein_interactor,
#             pmids=PMID,
#         )
#
#         response = self.client.get(
#             reverse(
#                 'protein-interactor',
#                 args=(protein_interactor.protein.uniprot,)),
#         )
#
#         pmid_link = "https://www.ncbi.nlm.nih.gov/pubmed/{0}".format(PMID)
#
#         self.assertContains(response, pmid_link, count=1)
#
#     def test_pmids_two(self):
#         """ Test that the ProteinInteractor view shows two PMID links correctly.
#         """
#
#         PMIDS = ["12345", "678910"]
#
#         protein_interactor = ProteinInteractorFactory.create(
#             annotated=True
#         )
#         DimerToProteinInteractorFactory.create(
#             protein_interactor=protein_interactor,
#             pmids="|".join(PMIDS),
#         )
#
#         response = self.client.get(
#             reverse(
#                 'protein-interactor',
#                 args=(protein_interactor.protein.uniprot,)),
#         )
#
#         for pmid in PMIDS:
#
#             pmid_link = "https://www.ncbi.nlm.nih.gov/pubmed/{0}".format(pmid)
#
#             self.assertContains(response, pmid_link, count=1)
#
#     def test_pdb_none(self):
#         """ Test that the ProteinInteractor view shows '(none)' if there are no
#         pbds
#         """
#
#         protein_interactor = ProteinInteractorFactory.create(pdb=None)
#
#         response = self.client.get(
#             reverse(
#                 'protein-interactor',
#                 args=(protein_interactor.protein.uniprot,)),
#         )
#
#         self.assertContains(response, "(none)", count=1)
#
#     def test_pdb_link_one_no_chain(self):
#         """ Test that the ProteinInteractor view shows a link to the PDB if
#         there is one pdb (without a chain specified).
#         """
#
#         PDB = "PDBX"
#
#         protein_interactor = ProteinInteractorFactory.create(pdb=PDB)
#
#         response = self.client.get(
#             reverse(
#                 'protein-interactor',
#                 args=(protein_interactor.protein.uniprot,)),
#         )
#
#         link = "https://www.rcsb.org/structure/{0}".format(PDB)
#
#         self.assertContains(response, link, count=1)
#
#     def test_pdb_link_one_with_chain(self):
#         """ Test that the ProteinInteractor view shows a link to the PDB if
#         there is one pdb (with a chain given).
#         """
#
#         PDB = "PDBX-Y"
#
#         protein_interactor = ProteinInteractorFactory.create(pdb=PDB)
#
#         response = self.client.get(
#             reverse(
#                 'protein-interactor',
#                 args=(protein_interactor.protein.uniprot,)),
#         )
#
#         link = "https://www.rcsb.org/structure/{0}".format(PDB.split("-")[0])
#
#         self.assertContains(response, link, count=1)
#
#     def test_pdb_link_two(self):
#         """ Test that the ProteinInteractor view shows two links to the PDB if
#         two pdbs are given.
#         """
#
#         PDBS = ["PDBX-A", "PDBY-B"]
#
#         protein_interactor = ProteinInteractorFactory.create(
#             pdb="|".join(PDBS)
#         )
#
#         response = self.client.get(
#             reverse(
#                 'protein-interactor',
#                 args=(protein_interactor.protein.uniprot,)),
#         )
#
#         for PDB in PDBS:
#             link = "https://www.rcsb.org/structure/{0}".format(
#                 PDB.split("-")[0]
#             )
#             self.assertContains(response, link, count=1)
#
#     def test_no_interactions_annotated(self):
#         """ Test that the correct warning message is shown if no annotations
#         are present (annotated=False).
#         """
#
#         expected = "no interactions annotated (yet)"
#
#         protein_interactor = ProteinInteractorFactory.create(
#             annotated=False
#         )
#
#         response = self.client.get(
#             reverse(
#                 'protein-interactor',
#                 args=(protein_interactor.protein.uniprot,)),
#         )
#
#         self.assertContains(response, expected, count=1)
#
#     def test_one_interaction_annotated(self):
#         """ Test that dimer name is shown if there is one interaction
#         annotated.
#         """
#
#         dimer = DimerFactory.create()
#
#         expected = dimer.display_name()
#
#         d2pi = DimerToProteinInteractorFactory.create(
#             protein_interactor__annotated=True,
#             dimer=dimer
#         )
#
#         response = self.client.get(
#             reverse(
#                 'protein-interactor',
#                 args=(d2pi.protein_interactor.protein.uniprot,)),
#         )
#
#         self.assertContains(response, expected, count=1)
#
#
# class ProteinInteractionListViewTest(TestCase):
#     """ Test ProteinInteraction list view
#     """
#
#     def test_proteininteraction_list_view_200(self):
#         """ Test that the ProteinInteractionListView returns 200
#         """
#
#         response = self.client.get(
#             reverse('protein-interactors')
#         )
#         self.assertEqual(response.status_code, 200)
#
#     def test_proteininteraction_list_uniprot_blast_link(self):
#         """ Test that the ProteinInteractionListView has a link to Uniprot
#         BLAST page
#         """
#
#         protein_interactions = ProteinInteractorFactory.create_batch(20)
#
#         response = self.client.get(
#             reverse('protein-interactors')
#         )
#
#         for protein_interaction in protein_interactions:
#             url = (
#                 "https://www.uniprot.org/blast/?"
#                 "about={0}[{1}-{2}]&amp;key=Motif"
#             )
#             expected = url.format(
#                 protein_interaction.protein.uniprot,
#                 protein_interaction.start,
#                 protein_interaction.stop,
#             )
#
#             self.assertContains(
#                 response, expected,
#                 msg_prefix="Did not find Uniprot link'{0}'".format(
#                     expected
#                 )
#             )
#
#     def test_proteininteraction_list_uniprot_link(self):
#         """ Test that the ProteinInteractionListView has a link to Uniprot
#         """
#
#         protein_interactions = ProteinInteractorFactory.create_batch(20)
#
#         response = self.client.get(
#             reverse('protein-interactors')
#         )
#
#         for protein_interaction in protein_interactions:
#             expected = "https://www.uniprot.org/uniprot/{0}".format(
#                 protein_interaction.protein.uniprot,
#             )
#             self.assertContains(
#                 response, expected,
#                 msg_prefix="Did not find Uniprot link'{0}'".format(
#                     expected
#                 )
#             )
#
#     def test_proteininteraction_list_contents_200(self):
#         """ Test that the ProteinInteractionListView shows all ProteinInteractions
#         """
#
#         protein_interactions = ProteinInteractorFactory.create_batch(20)
#
#         response = self.client.get(
#             reverse('protein-interactors')
#         )
#
#         for protein_interaction in protein_interactions:
#             self.assertContains(
#                 response, protein_interaction.protein.uniprot,
#                 msg_prefix="Did not find name '{0}'".format(
#                     protein_interaction.name,
#                 )
#             )
#             self.assertContains(
#                 response, protein_interaction.taxonomic_group,
#                 msg_prefix="Did not find taxonomic_group '{0}'".format(
#                     protein_interaction.taxonomic_group
#                 )
#             )
#             self.assertContains(
#                 response, protein_interaction.protein.uniprot,
#                 msg_prefix="Did not find uniprot '{0}'".format(
#                     protein_interaction.protein.uniprot
#                 )
#             )
#             motif_location = "{0}-{1}".format(
#                 protein_interaction.start,
#                 protein_interaction.stop,
#             )
#             self.assertContains(
#                 response, motif_location,
#                 msg_prefix="Did not find motif location'{0}'".format(
#                     motif_location
#                 )
#             )
#             self.assertContains(
#                 response, protein_interaction.site_definition,
#                 msg_prefix="Did not find site_definition '{0}'".format(
#                     protein_interaction.site_definition,
#                 )
#             )
