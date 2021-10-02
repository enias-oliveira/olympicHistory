from django.db import models

from athletes.models import Athlete
from games.models import Event


class Medal(models.Model):
    GOLD = "Gold"
    SILVER = "Silver"
    BRONZE = "Bronze"

    MEDAL_CLASS_CHOICES = (
        ("G", GOLD),
        ("S", SILVER),
        ("B", BRONZE),
    )

    medal_class = models.CharField(max_length=1, choices=MEDAL_CLASS_CHOICES)

    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    athletes = models.ManyToManyField(Athlete, related_name="medals")
