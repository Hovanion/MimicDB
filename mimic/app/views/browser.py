from app.models import ProteinInteractor, ProteinInformation, Protein

from django.views.generic import ListView

CELL_BASED_ASSAY = (
    "Adhesion assay evidence",
    "Cell aggregation evidence",
    "Cell-based assay evidence",
    "Cell proliferation assay evidence",
    "Chemotaxis assay evidence",
    "Plaque assay evidence",
)

PURIFIED_ASSAY = (
    "Affinity chromatography evidence",
    "Bait-prey protein pull-down assay evidence",
    "Bio-layer interferometry assay evidence",
    "Co-immunoprecipitation evidence",
    "Co-localization evidence",
    "Cryogenic electron microscopy evidence",
    "Enzyme-linked immunoabsorbent assay evidence",
    "Flow cytometry evidence",
    "Fluorescence anisotropy evidence",
    "Fluorescence polarization evidence",
    "Fluorescence resonance energy transfer evidence",
    "Gel-filtration evidence",
    "Immunofluorescence confocal microscopy evidence",
    "Immunoprecipitation evidence",
    "Iodine-125-labeled ligand binding assay evidence",
    "Isothermal titration calorimetry evidence",
    "Nuclear magnetic resonance spectroscopy evidence",
    "Peptide array evidence",
    "Phage display evidence",
    "Protein hydrogen-deuterium exchange mass spectrometry evidence",
    "Protein inhibition evidence",
    "Quantitative western immunoblotting evidence",
    "Radioligand binding assay evidence",
    "Small-angle X-ray scattering evidence",
    "Sodium dodecyl sulfate polyacrylamide gel electrophoresis evidence",
    "Surface plasmon resonance evidence",
    "X-ray crystallography evidence",
)


class BrowserView(ListView):
    template_name = 'app/browser.html'
    paginate_by = 50
    model = ProteinInteractor
    context_object_name = 'records'

    def get_queryset(self):
        data_rows = ProteinInteractor.objects.values().distinct()
        data = list()
        print(len(data_rows))
        hit = set()
        for row in data_rows:
            protein_data = Protein.objects.filter(id=row["protein_id"]).all().first()
            if protein_data.uniprot not in hit:
                hit.add(protein_data.uniprot)
            else:
                if protein_data.peptide not in hit:
                    hit.add(protein_data.peptide)
                else:
                    continue

            adat = {"protein": protein_data.uniprot, "peptide": protein_data.peptide, "id": protein_data.id,
                    "organism": "-", "name": "-"}

            if protein_data.uniprot != "-":
                information = ProteinInformation.objects.filter(protein_id=row["protein_id"]).all().first()
                adat["organism"] = information.organism_scientific
                adat["name"] = information.name
            adat["type_of_interaction"] = row["type_of_interaction"]
            expmethod = ProteinInteractor.objects.filter(protein_id=row['protein_id']).values_list(
                "experimental_method").distinct().order_by("experimental_method")
            adat["experimental_method"] = ', '.join(str(item[0]) for item in expmethod)
            integrins = ProteinInteractor.objects.filter(protein_id=row["protein_id"]).values_list(
                "target_integrin").distinct().order_by("target_integrin")

            adat["integrins"] = ', '.join(
                str(item[0].replace("alpha-", "&alpha;").replace("beta-", "&beta;")) for item in integrins)

            adat["interaction_strength"] = False
            if ProteinInteractor.objects.filter(protein_id=row["protein_id"],
                                                interaction_strength__icontains="=").values_list(
                "interaction_strength").distinct().count() > 0:
                adat["interaction_strength"] = True

            adat["bound_structure"] = False
            if ProteinInteractor.objects.filter(protein_id=row["protein_id"], xref__icontains="PDB").values_list(
                    "interaction_strength").distinct().count() > 0:
                adat["bound_structure"] = True
            adat["cell_based_assay"] = False
            adat["purified_assay"] = False
            for method in expmethod:
                if method[0] in CELL_BASED_ASSAY:
                    adat["cell_based_assay"] = True
                if method[0] in PURIFIED_ASSAY:
                    adat["purified_assay"] = True

            data.append(adat)

        return data

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
