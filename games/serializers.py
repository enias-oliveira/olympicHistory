from rest_framework import serializers

from .models import Game, Sport, Event, Competition


class GameCompetitionSerializer(serializers.ModelSerializer):
    event_id = serializers.SerializerMethodField()
    sport = serializers.SlugRelatedField(slug_field="name", read_only=True)
    competition = serializers.CharField(source="name", read_only=True)

    class Meta:
        model = Competition
        fields = ["event_id", "competition", "sport"]

    def get_event_id(self, obj: Competition):
        event = Event.objects.get(competition=obj)
        return event.id


class GameSerializer(serializers.ModelSerializer):
    events = GameCompetitionSerializer(many=True)

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
