from django.db import models


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
