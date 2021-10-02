from rest_framework import serializers

from medals.models import Medal
from medals.serializers import MedalSerializer
from games.models import Event
from games.serializers import EventSerializer

from .models import Athlete, Country


class AthleteMedalSerializer(MedalSerializer):
    class Meta:
        model = Medal
        fields = ["id", "medal_class", "event"]


class CountrySerializer(serializers.ModelSerializer):
    class Meta():
        model = Country
        fields = ["noc", "name"]


class AthleteCountryField(serializers.RelatedField):
    queryset = Country.objects.all()

    def to_representation(self, value):
        serialized_country = CountrySerializer(value)
        return serialized_country.data

    def to_internal_value(self, data):
        return self.queryset.get(name=data)


class AthleteMedalsField(serializers.RelatedField):
    queryset = Medal.objects.all()

    def to_representation(self, value):
        serialized_medal = AthleteMedalSerializer(value)
        return serialized_medal.data

    def to_internal_value(self, data):
        return self.queryset.get(pk=data)


class AthleteEventsField(serializers.RelatedField):
    queryset = Event.objects.all()

    def to_representation(self, value: Event):
        value.sport = value.competition.sport.name
        serialized_medal = EventSerializer(value)
        return serialized_medal.data

    def to_internal_value(self, data):
        return self.queryset.get(pk=data)


class AthleteSerializer(serializers.ModelSerializer):
    medals = AthleteMedalsField(many=True, required=False)
    events = AthleteEventsField(many=True, required=False)
    country = AthleteCountryField()

    class Meta:
        model = Athlete
        fields = "__all__"
