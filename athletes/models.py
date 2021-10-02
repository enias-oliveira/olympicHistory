from django.db import models

from games.models import Event


class Country(models.Model):
    name = models.CharField(max_length=255)
    noc = models.CharField(max_length=3)
    notes = models.CharField(max_length=255, blank=True)


class Athlete(models.Model):
    MALE = "Male"
    FEMALE = "Female"
    SEX_CHOICES = (
        ("M", MALE),
        ("F", FEMALE),
    )

    name = models.CharField(max_length=255)
    sex = models.CharField(max_length=1, choices=SEX_CHOICES)
    age = models.PositiveIntegerField()
    height = models.PositiveIntegerField(null=True, blank=True)
    weight = models.PositiveIntegerField(null=True, blank=True)

    country = models.ForeignKey(
        Country,
        on_delete=models.RESTRICT,
        related_name="athletes",
    )

    events = models.ManyToManyField(Event, related_name="athletes")
