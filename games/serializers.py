from rest_framework import serializers

from .models import Game


class GameSerializer(serializers.ModelSerializer):
    events = serializers.SerializerMethodField()

    class Meta:
        model = Game
        fields = "__all__"
        depth = 2
