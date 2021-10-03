from rest_framework import serializers

from .models import Game, Sport, Competition, Event


class GameEventSerializer(serializers.ModelSerializer):
    competition_id = serializers.IntegerField(source="id", read_only=True)
    sport = serializers.SlugRelatedField(
        slug_field="name",
        read_only=True
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

    def to_representation(self, instance):
        current_representation = super().to_representation(instance)

        current_representation["season"] = dict(Game.SEASON_CHOICES)[
            current_representation["season"]
        ]

        return current_representation

    def to_internal_value(self, data):
        if data.get("season"):
            season_full_to_short = {v: k for k, v in Game.SEASON_CHOICES}
            data["season"] = season_full_to_short[data["season"]]

        return data


class EventGameSerializer(GameSerializer):
    events = None

    class Meta():
        model = Game
        exclude = ["events"]


class EventSerializer(serializers.ModelSerializer):
    sport = serializers.CharField()
    game = EventGameSerializer(read_only=True)
    competition = serializers.CharField(source="competition_name")

    class Meta:
        model = Event
        fields = "__all__"
