from app.models import ProteinInformation
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = ('Delete all Protein Information.')

    def handle(self, *args, **options):
        ProteinInformation.objects.all().delete()

        self.stdout.write("Deleted all ProteinInformation.")
