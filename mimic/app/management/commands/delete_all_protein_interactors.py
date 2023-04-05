from django.core.management.base import BaseCommand

from app.models import ProteinInteractor


class Command(BaseCommand):
    help = ('Delete all ProteinInteractors.')

    def handle(self, *args, **options):

        ProteinInteractor.objects.all().delete()

        self.stdout.write("Deleted all ProteinInteractors.")
