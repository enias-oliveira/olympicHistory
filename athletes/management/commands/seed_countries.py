import csv

from django.core.management.base import BaseCommand

from ...models import Country


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            "csvfile",
            type=str,
            help="Path to CSV file with countries",
        )

    def handle(self, *args, **kwargs):
        csv_file_path = kwargs["csvfile"]

        print(f"Seeding Countries from {csv_file_path}")

        with open(csv_file_path, "r") as file:
            csv_countries = csv.DictReader(file)

            def create_country_obj(csv_country):
                return Country(
                    name=csv_country["region"].strip(),
                    noc=csv_country["NOC"].strip(),
                    notes=csv_country["notes"].strip(),
                )

            countries = [create_country_obj(cc) for cc in csv_countries]

            print(f"Creating { len(countries) } Country Objects")

            try:
                Country.objects.bulk_create(countries)
                print("Countries Seeding succesfull")
            except Exception:
                print("Seed Failed, Exception")
                print(Exception)
