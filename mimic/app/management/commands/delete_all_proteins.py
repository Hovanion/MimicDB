from django.core.management.base import BaseCommand

from app.models import Protein


class Command(BaseCommand):
    help = ('Delete all Protein.')

    def handle(self, *args, **options):

        Protein.objects.all().delete()

        self.stdout.write("Deleted all Protein.")
