from rest_framework import serializers

from .models import Game, Sport, Event


class SportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sport
        fields = ["name"]


class EventSerializer(serializers.ModelSerializer):
    sport = SportSerializer(many=True)

    class Meta:
        model = Event
        fields = "__all__"


class GameEventField(serializers.RelatedField):
    def to_representation(self, value: Competition):
        event = Event.objects.get(competition=value)

        serialized_game_event = {
            "id": event.id,
            "competition": value.name,
            "sport": value.sport.name,
        }

        return serialized_game_event


class GameSerializer(serializers.ModelSerializer):
    events = GameEventField(many=True, read_only=True)

    class Meta:
        model = Game
        fields = "__all__"
