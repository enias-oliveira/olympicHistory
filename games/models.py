from django.db import models


class Sport(models.Model):
    name = models.CharField(max_length=255)


class Competition(models.Model):
    name = models.CharField(max_length=255)

    sport = models.ForeignKey(
        Sport, on_delete=models.RESTRICT, related_name="competitions"
    )


class Game(models.Model):
    SUMMER = "Summer"
    WINTER = "Winter"

    SEASON_CHOICES = (
        ("S", SUMMER),
        ("W", WINTER),
    )

    city = models.CharField(max_length=255)
    year = models.PositiveIntegerField()
    season = models.CharField(max_length=6, choices=SEASON_CHOICES)

    events = models.ManyToManyField(Competition, db_table="events")
