from django.core.management.base import BaseCommand
from skillsbridge_core.loaders import load_smu_igp

class Command(BaseCommand):
    help = "Import SMU IGP into the DB"

    def handle(self, *args, **options):
        self.stdout.write("Starting data import …")
        load_smu_igp("data/smu_igp_2024.html")
        self.stdout.write("Finished import.")

