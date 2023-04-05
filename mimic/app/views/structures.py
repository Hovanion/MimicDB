from app.models import Pdb, PdbToProtein, Monomer
from django.shortcuts import render


def StructureView(request):
    data = Pdb.objects.values()

    context = {'records': list()}
    for row in data:
        adat = {"pdb": row['pdb']}
        adat["exp_tech"] = row['exp_tech']
        adat["resolution"] = row['resolution']
        interactions = PdbToProtein.objects.filter(pdb__pdb=row['pdb'])
        if interactions.exists():
            adat["interaction"] = list()
            for entry in interactions:
                adat["interaction"].append(entry.protein.uniprot.strip())
        else:
            adat["interaction"] = "-"

        adat["alpha_subunit"] = Monomer.objects.filter(id=row["alpha_id"]).all().first()
        adat["beta_subunit"] = Monomer.objects.filter(id=row["beta_id"]).all().first()
        adat["protein_interactors"] = False
        adat["other_interactors"] = False

        if row["other_interactors"]:
            if "protein" in row["other_interactors"]:
                adat["protein_interactors"] = True
            else:
                adat["other_interactors"] = True

        context['records'].append(adat)

    return render(request, 'app/pdb_list.html', context)
