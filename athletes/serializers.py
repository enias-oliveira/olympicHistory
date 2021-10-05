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
    class Meta:
        model = Country
        fields = ["id", "name", "noc"]


class AthleteCountrySerializer(CountrySerializer):
    class Meta:
        model = Country
        fields = ["noc", "name"]


class AthleteEventSerializer(EventSerializer):
    competition = serializers.SlugRelatedField(
        slug_field="name",
        read_only=True,
    )

    class Meta:
        model = Event
        fields = "__all__"


class AthleteRelatedField(serializers.RelatedField):
    def to_representation(self, value):
        serialized_data = self.serializer_class(value)
        return serialized_data.data

    def to_internal_value(self, data):
        return self.queryset.get(pk=data)


class AthleteCountryField(AthleteRelatedField):
    queryset = Country.objects.all()
    serializer_class = AthleteCountrySerializer

    def to_internal_value(self, data):
        return self.queryset.get(name=data)


class AthleteMedalsField(AthleteRelatedField):
    queryset = Medal.objects.all()
    serializer_class = AthleteMedalSerializer


class AthleteEventsField(AthleteRelatedField):
    queryset = Event.objects.all()
    serializer_class = AthleteEventSerializer

    def to_representation(self, value):
        value.sport = value.competition.sport.name
        serialized_data = self.serializer_class(value)
        return serialized_data.data


class AthleteSerializer(serializers.ModelSerializer):
    medals = AthleteMedalsField(many=True, required=False)
    events = AthleteEventsField(many=True, required=False)
    country = AthleteCountryField()

    class Meta:
        model = Athlete
        fields = "__all__"
