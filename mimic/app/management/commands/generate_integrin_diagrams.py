import os

from django.core.management.base import BaseCommand
from django.conf import settings

from app.models import Dimer


INTEGRINS_PATH = os.path.join(
    settings.BASE_DIR, 'mimic', 'static', 'mimic', 'integrins'
)


class Command(BaseCommand):
    help = (
        """Generates *png images of all Dimer objects, and saves them to',
        'static/integrins'."""
    )

    def _generate_integrins(self):
        """ Parse and upload Dimer instancse.
        """

        for dimer in Dimer.objects.all():
            filename = "{0}.png".format(dimer.lookup_name)
            filepath = os.path.join(INTEGRINS_PATH, filename)
            dimer.generate_dimer_thumbnail(filepath)

            self.stdout.write("Created thumbnail: {0}\n".format(filepath))

    def handle(self, *args, **options):

        self._generate_integrins()
