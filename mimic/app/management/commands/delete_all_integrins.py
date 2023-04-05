from django.core.management.base import BaseCommand

from app.models import Monomer
from app.models import Dimer
from app.models import Structure


class Command(BaseCommand):
    help = ('Delete all contents of Monomers, Dimers and Structures.')

    def handle(self, *args, **options):

        Monomer.objects.all().delete()
        Dimer.objects.all().delete()
        Structure.objects.all().delete()

        self.stdout.write("Deleted all Integrin data.")
