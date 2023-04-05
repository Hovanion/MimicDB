import os

from django.core.management.base import BaseCommand, CommandError

from app.parsers import StructureParser  #pylint: disable


class Command(BaseCommand):
    help = (
        'Uploads data for Integrin Structures from an excel sheet. See the '
        'mimicDB docs and StructureParser docs for more information on the '
        'format of the file to upload.'
    )

    def add_arguments(self, parser):
        parser.add_argument(
            'filename',
            type=str,
            help="Name and path of file to upload"
        )

    @staticmethod
    def _check_file(filename):
        """ Make sure that a file with 'filename' exists. raises a CommandError
        if it does not.
        """

        if not os.path.exists(filename):
            raise CommandError("Could not find file: {0}".format(filename))

    def _parse_monomers(self, filename):
        """ Parse and upload Monomer instancse.
        """

        monomer_parser = StructureParser(filename)
        monomer_parser.parse_and_upload()

        self.stdout.write("\n".join(monomer_parser.messages))

    def handle(self, *args, **options):

        filename = options['filename']

        self._check_file(filename)
        self._parse_monomers(filename)
