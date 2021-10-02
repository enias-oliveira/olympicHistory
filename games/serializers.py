from rest_framework import serializers

from .models import Game, Sport, Competition, Event


class GameEventSerializer(serializers.ModelSerializer):
    competition_id = serializers.IntegerField(source="id", read_only=True)
    sport = serializers.SlugRelatedField(
        slug_field="name",
        queryset=Sport.objects.all(),
    )
    competition = serializers.CharField(source="name")

    class Meta:
        model = Competition
        fields = ["competition_id", "competition", "sport"]


class GameSerializer(serializers.ModelSerializer):
    events = GameEventSerializer(many=True)

    class Meta:
        model = Game
        fields = "__all__"

    def create(self, validated_data):
        validated_data.pop("events")
        game = Game.objects.get_or_create(**validated_data)[0]

        raw_events = self.initial_data.get("events")

        def create_competition(evt):
            sport = Sport.objects.get_or_create(name=evt["sport"])[0]
            return Competition.objects.get_or_create(
                name=evt["competition"],
                sport=sport,
            )[0]

        game.events.set([create_competition(evt) for evt in raw_events])

        return game


class EventSerializer(serializers.ModelSerializer):
    competition = serializers.SlugRelatedField(
        slug_field="name",
        queryset=Sport.objects.all(),
    )
    sport = serializers.CharField()

    class Meta:
        model = Event
        fields = "__all__"
