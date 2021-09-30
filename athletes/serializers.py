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
        country_data = validated_data.get("country")
        country = Country.objects.get(name=country_data.get("name"))

        # Functional Approach of creating new dict
        athlete_data = {
            item: validated_data[item] for item in validated_data if item != "country"
        }
        athlete = Athlete.objects.create(**athlete_data, country=country)

        return athlete
