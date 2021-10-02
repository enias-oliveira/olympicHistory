from rest_framework import serializers

from .models import Game, Sport, Competition


class EventSerializer(serializers.ModelSerializer):
    competition_id = serializers.IntegerField(source="id",read_only=True)
    competition = serializers.CharField(source="name", read_only=True)
    sport = serializers.SlugRelatedField(slug_field="name", read_only=True)

    class Meta:
        model = Competition
        fields = ["competition_id", "competition", "sport"]


class GameSerializer(serializers.ModelSerializer):
    events = EventSerializer(many=True)

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
                name=evt["name"],
                sport=sport,
            )[0]

        game.events.set([create_competition(evt) for evt in raw_events])

        return game


class GameEventSerializer(serializers.Serializer):
    competition = serializers.CharField(required=True)
    sport = serializers.CharField(required=True)
