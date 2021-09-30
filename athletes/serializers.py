from rest_framework import serializers

from .models import Athlete, Country


class AthleteCountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ["name", "noc"]


class AthleteSerializer(serializers.ModelSerializer):
    country = AthleteCountrySerializer()

    class Meta:
        model = Athlete
        fields = "__all__"

    def create(self, validated_data):
        country_data = validated_data.pop("country")
        country = Country.objects.get(name=country_data.get("name"))

        athlete = Athlete.objects.create(**validated_data, country=country)

        return athlete
