import re

from app.models import ProteinInteractor, ProteinInformation, Protein
from django.views.generic import TemplateView


class InteractionsView(TemplateView):
    template_name = 'app/interactions.html'

    def get_context_data(self, **kwargs):
        entry_id = kwargs['protein']

        if re.match("\d+", entry_id):
            data = {"entry": Protein.objects.filter(id=entry_id).values().first()}
            data["peptide"] = True
            data["records"] = ProteinInteractor.objects.filter(protein_id=entry_id)

        else:
            data = {"entry": ProteinInteractor.objects.filter(protein__uniprot=entry_id).all().first()}
            data["peptide"] = False
            data["records"] = ProteinInteractor.objects.filter(protein__uniprot=entry_id)

            data["information"] = ProteinInformation.objects.filter(protein__uniprot=entry_id).first()

        return data
