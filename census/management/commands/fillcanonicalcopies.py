from django.core.management.base import BaseCommand, CommandError
from census.ingest.canonical_copy import export_old_copies

class Command(BaseCommand):
    help = ('Export the old copy json file and then'
             'store it into the new cannonical copy models')

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        export_old_copies()
