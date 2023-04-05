import os

from django.core.management.base import BaseCommand, CommandError

from app.parsers import ProteinInteractorParser


class Command(BaseCommand):
    help = (
        'Uploads data for Protein Interactors from an excel sheet. See the '
        'mimicDB docs and ProteinInteractorParser docs for more information '
        'on the format of the file to upload.'
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

    def _parse_protein_interactors(self, filename):
        """ Parse and upload ProteinInteractor objects.
        """

        protein_interactor_parser = ProteinInteractorParser(filename)
        protein_interactor_parser.parse_and_upload()

        self.stdout.write("\n".join(protein_interactor_parser.messages))

    def handle(self, *args, **options):

        filename = options['filename']

        self._check_file(filename)
        self._parse_protein_interactors(filename)
