import os

from app.parsers import ProteinInformationParser
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = (
        'Uploads data for Protein Information from an excel sheet. '
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

    def _parse_protein_information(self, filename):
        """ Parse and upload ProteinInformation objects.
        """

        protein_information_parser = ProteinInformationParser(filename)
        protein_information_parser.parse_and_upload()

        self.stdout.write("\n".join(protein_information_parser.messages))

    def handle(self, *args, **options):
        filename = options['filename']

        self._check_file(filename)
        self._parse_protein_information(filename)
