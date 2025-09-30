from django.core.management.base import BaseCommand
from skillsbridge_core.loaders import load_all

class Command(BaseCommand):
    help = "Import all configured datasets from data.gov.sg into the DB"

    def handle(self, *args, **options):
        self.stdout.write("Starting data import …")
        load_all()
        self.stdout.write("Finished import.")
