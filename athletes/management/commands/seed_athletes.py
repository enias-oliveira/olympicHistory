import dask.dataframe as dd
import numpy as np

from django.db.models import Q
from django.core.management.base import BaseCommand

from ...models import Athlete, Country

from games.models import Sport, Competition, Game, Event

from medals.models import Medal


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

        games_data = raw_athletes_df[["City", "Year", "Season"]].copy()
        unique_games_data = games_data.drop_duplicates(subset=["Year"])
        print("Creating Games...")
        Game.objects.bulk_create(
            [
                Game(
                    city=uni_game.City,
                    year=uni_game.Year,
                    season=uni_game.Season[0],
                )
                for i, uni_game in unique_games_data.iterrows()
            ],
            ignore_conflicts=True,
        )
        total_games = Game.objects.all().count()
        print(f"Total Games Created: {total_games}")

        print("Creating Sports...")
        unique_sport_data = raw_athletes_df["Sport"].unique()
        Sport.objects.bulk_create(
            [Sport(name=uni_sport) for uni_sport in unique_sport_data],
            ignore_conflicts=True,
        )
        total_sports = Sport.objects.all().count()
        print(f"Total Sports in DB: {total_sports}")

        print("Creating Competitions...")
        competitions_data = raw_athletes_df[["Sport", "Event"]].copy()
        unique_competitions_data = competitions_data.drop_duplicates()
        Competition.objects.bulk_create(
            [
                Competition(
                    name=uni_competition.Event,
                    sport=Sport.objects.get(name=uni_competition.Sport),
                )
                for i, uni_competition in unique_competitions_data.iterrows()
            ],
            ignore_conflicts=True,
        )
        total_competitions = Competition.objects.all().count()
        print(f"Total Competitions in DB: {total_competitions}")

        print("Creating Events...")
        event_count = 0
        events_data = raw_athletes_df[["Year", "Event"]].copy()
        unique_events = events_data.drop_duplicates()
        events_queue = []

        def create_event_obj(uni_event):
            return Event(
                game=Game.objects.get(year=uni_event.Year),
                competition=Competition.objects.get(name=uni_event.Event),
            )

        for i, uni_event in unique_events.iterrows():
            event_count += 1
            if event_count % 1000 == 0:
                print(f"Events Created: {event_count}")

            events_queue.append(create_event_obj(uni_event))

        Event.objects.bulk_create(events_queue, ignore_conflicts=True)
        total_events = Event.objects.all().count()
        print(f"Total Events in DB: {total_events}")

        print("Creating Medals...")
        medal_count = 0
        medals_data = raw_athletes_df[["Year", "Event", "Medal"]].copy()
        unique_medals_data = medals_data.dropna(
            subset=["Medal"],
        ).drop_duplicates()
        medal_queue = []

        def create_medal_obj(uni_medal):
            game = Game.objects.get(year=uni_medal.Year)
            competition = Competition.objects.get(name=uni_medal.Event)
            event = Event.objects.get(game=game, competition=competition)

            return Medal(medal_class=uni_medal.Medal[0], event=event)

        for i, uni_medal in unique_medals_data.iterrows():
            medal_count += 1
            if event_count % 1000 == 0:
                print(f"Medals Created: {medal_count}")

            medal_queue.append(create_medal_obj(uni_medal))

        Medal.objects.bulk_create(
            medal_queue,
            ignore_conflicts=True,
        )

        total_medals = Medal.objects.all().count()
        print(f"Total Medals in DB: {total_medals}")

        print("Creating Athletes...")
        athletes_count = 0
        athletes_data = raw_athletes_df[
            [
                "Name",
                "Sex",
                "Height",
                "Weight",
                "NOC",
            ]
        ].copy()
        unique_athletes_data = athletes_data.drop_duplicates()
        athletes_queue = []

        def create_athlete_obj(uni_athlete_data):
            athlete_country = Country.objects.get(
                noc=uni_athlete_data.NOC.strip(),
            )

            def convert_float_to_int_or_none(flt):
                return int(flt) if not np.isnan(flt) else None

            return Athlete(
                name=uni_athlete_data.Name.strip(),
                sex=uni_athlete_data.Sex.strip(),
                height=convert_float_to_int_or_none(uni_athlete_data.Height),
                weight=convert_float_to_int_or_none(uni_athlete_data.Weight),
                country=athlete_country,
            )

        for uni_athlete in unique_athletes_data.iterrows():
            if Country.objects.filter(noc=uni_athlete[1].NOC.strip()).exists():
                athletes_count += 1
                if athletes_count % 10000 == 0:
                    print(f"Athletes Created: {athletes_count}")
                athletes_queue.append(create_athlete_obj(uni_athlete[1]))

        Athlete.objects.bulk_create(
            athletes_queue,
            ignore_conflicts=True,
        )
        total_athletes = Athlete.objects.all().count()
        print(f"Total Athletes in DB: {total_athletes}")

        print("Creating Athletes, Medals and Events Relationship")
        athlete_events_count = 0
        athlete_medals_count = 0
        athletes_events_data = raw_athletes_df[
            ["Name", "Year", "Event", "Medal"]
        ].copy()
        grouped_athletes_events = athletes_events_data.groupby("Name").agg(list)
        athlete_events_queue = []
        athlete_medals_queue = []

        for ath_event in grouped_athletes_events.iterrows():
            name, data = ath_event
            data_combined = zip(data.Year, data.Event, data.Medal)

            if Athlete.objects.filter(name=name).exists():
                athlete = Athlete.objects.get(name=name)

                events = []
                medals = []

                for d in data_combined:
                    athlete_events_count += 1
                    if athlete_events_count % 50_000 == 0:
                        print(
                            f"Athletes Events Relation Created: {athlete_events_count}"
                        )

                    year, event, medal = d
                    cur_event = Event.objects.filter(
                        Q(game__year__exact=year) & Q(competition__name__exact=event)
                    )[0]

                    events.append(cur_event)

                    if isinstance(medal, str):
                        athlete_medals_count += 1
                        if athlete_medals_count % 5_000 == 0:
                            print(
                                f"Athletes Medals Relation Created: {athlete_medals_count}"
                            )
                        medals.append(
                            Medal.objects.get(
                                medal_class=medal[0],
                                event=cur_event,
                            )
                        )

                athlete_events_queue += [
                    Athlete.events.through(
                        athlete_id=athlete.pk,
                        event_id=evt.pk,
                    )
                    for evt in events
                ]

                athlete_medals_queue += [
                    Athlete.medals.through(
                        athlete_id=athlete.pk,
                        medal_id=mdl.pk,
                    )
                    for mdl in medals
                ]

        Athlete.events.through.objects.bulk_create(
            athlete_events_queue,
            ignore_conflicts=True,
        )

        Athlete.medals.through.objects.bulk_create(
            athlete_medals_queue,
            ignore_conflicts=True,
        )

        print("Finished")
