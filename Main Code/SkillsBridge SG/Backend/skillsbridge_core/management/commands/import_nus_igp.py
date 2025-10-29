from django.core.management.base import BaseCommand
from skillsbridge_core.loaders import load_nus_igp

class Command(BaseCommand):
    help = "Import NUS IGP into the DB"

    def handle(self, *args, **options):
        self.stdout.write("Starting data import …")
        load_nus_igp("data/nus_igp_2024.html")
        self.stdout.write("Finished import.")

