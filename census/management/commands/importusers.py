from django.core.management.base import BaseCommand, CommandError
from census.ingest.serialize import import_user_json

class Command(BaseCommand):
    help = ('Import a json version of the current database. '
            'NOTE: This does not currently preserve important '
            'information about where the data came from, and so '
            'librarian validated data will not be identified '
            'as such, and will have to be re-checked.')

    def add_arguments(self, parser):
        parser.add_argument('json_basename')

    def handle(self, *args, **options):
        import_user_json(options['json_basename'])
