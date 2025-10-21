from django.core.management.base import BaseCommand
from skillsbridge_core.loaders import load_sit_igp

class Command(BaseCommand):
    help = "Import SIT IGP into the DB"

    def handle(self, *args, **options):
        self.stdout.write("Starting data import …")
        load_sit_igp("data/sit_igp_2024.pdf")
        self.stdout.write("Finished import.")

