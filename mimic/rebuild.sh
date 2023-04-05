#!/bin/bash
#rm db.sqlite3
python manage.py migrate
python manage.py delete_all_integrins
python manage.py delete_all_drugs
python manage.py delete_all_protein_interactors
python manage.py delete_all_proteins_information
python manage.py delete_all_proteins

echo "--------- ALL DATA WAS DELETED"
#
python manage.py upload_structures all-data/domain_shorthands.xlsx
#OK

python manage.py upload_monomers all-data/integrin_monomers.xlsx
#OK

python manage.py upload_dimers all-data/integrin_dimers.xlsx
#OK

python manage.py upload_drugs all-data/integrin_drugs.xlsx
#OK

python manage.py upload_protein_information all-data/data_for_protein.xlsx
#OK
python manage.py upload_pdbs all-data/integrin_structures.xlsx

python manage.py upload_protein_interactors all-data/data_test_2022.07.27.xlsx
#OK

