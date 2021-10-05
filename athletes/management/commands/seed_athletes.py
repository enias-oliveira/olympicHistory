import dask
import dask.dataframe as dd
import numpy as np

from django.core.management.base import BaseCommand
from django.db.models import Q

from ...models import Athlete, Country

from games.models import Sport, Competition, Game


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            "csvfile",
            type=str,
            help="Path to CSV file with Athletes",
        )

    def handle(self, *args, **kwargs):
        csv_file_path = kwargs["csvfile"]

        raw_athletes_df = dd.read_csv(csv_file_path, dtype={"Age": "float64"})

        print(f"Seeding Athletes and Related from {csv_file_path}")

        total_rows = len((raw_athletes_df.index))
        print(f"Total Rows: { total_rows }")

        @dask.delayed
        def create_athletes_and_related(raw_athletes_batch):

            print("Creating Athletes...")

            def create_athlete_obj(raw_athlete):
                raw_athlete_data = raw_athlete[1]

                athlete_country = Country.objects.get(noc=raw_athlete_data.NOC.strip())

                def convert_float_to_int_or_none(flt):
                    return int(flt) if not np.isnan(flt) else None

                return Athlete(
                    name=raw_athlete_data.Name.strip(),
                    sex=raw_athlete_data.Sex.strip(),
                    age=convert_float_to_int_or_none(raw_athlete_data.Age),
                    height=convert_float_to_int_or_none(raw_athlete_data.Height),
                    weight=convert_float_to_int_or_none(raw_athlete_data.Weight),
                    country=athlete_country,
                )

            athletes = [
                create_athlete_obj(raw_athlete)
                for raw_athlete in raw_athletes_batch.iterrows()
                if Country.objects.filter(noc=raw_athlete[1].NOC.strip()).exists()
            ]

            self.stdout.write(f"Processed Rows from CSV: {raw_athletes_batch.iloc[-1].ID}")

            created_athletes = Athlete.objects.bulk_create(
                athletes,
                ignore_conflicts=True,
            )

            self.stdout.write(f"New Athletes Created: {len(created_athletes)}")


            # def create_competition_obj(raw_athlete):
            #     return Competition(
            #         name=
            #     )

            # competitions = [
            #     create_competition_obj(raw_athlete) for raw_athlete in raw_athletes_batch.iterrows()
            # ]

        #     # sports
        #     # games =
        #     # medals

        dask.compute(
            [
                create_athletes_and_related(raw_athletes_batch)
                for raw_athletes_batch in raw_athletes_df.to_delayed()
            ]
        )
