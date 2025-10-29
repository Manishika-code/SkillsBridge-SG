from django.core.management.base import BaseCommand
from skillsbridge_core.loaders import load_ntu_igp

class Command(BaseCommand):
    help = "Import NTU IGP into the DB"

    def handle(self, *args, **options):
        self.stdout.write("Starting data import …")
        load_ntu_igp()
        self.stdout.write("Finished import.")
