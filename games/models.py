from django.db import models


class Sport(models.Model):
    name = models.CharField(max_length=255, unique=True)


class Competition(models.Model):
    name = models.CharField(max_length=255, unique=True)

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
    year = models.PositiveIntegerField(unique=True)
    season = models.CharField(max_length=6, choices=SEASON_CHOICES)

    events = models.ManyToManyField(
        Competition, through="Event", through_fields=("game", "competition")
    )


class Event(models.Model):
    game = models.ForeignKey(Game, on_delete=models.RESTRICT)
    competition = models.ForeignKey(Competition, on_delete=models.RESTRICT)
