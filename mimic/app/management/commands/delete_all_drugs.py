from django.core.management.base import BaseCommand

from app.models import Drug

class Command(BaseCommand):
    help = ('Delete all contents Drugs.')

    def handle(self, *args, **options):

        Drug.objects.all().delete()

        self.stdout.write("Deleted all Drug data.")
