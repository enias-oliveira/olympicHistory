from rest_framework import serializers

from games.models import Event

from .models import Medal


class MedalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medal
        fields = "__all__"

    def to_representation(self, instance):
        current_representation = super().to_representation(instance)

        current_representation["medal_class"] = dict(Medal.MEDAL_CLASS_CHOICES)[
            current_representation["medal_class"]
        ]

        return current_representation

    def to_internal_value(self, data):
        if data.get("medal_class"):
            medal_full_to_short = {v: k for k, v in Medal.MEDAL_CLASS_CHOICES}
            data["medal_class"] = medal_full_to_short[data["medal_class"]]

        if data.get("event"):
            data["event"] = Event.objects.get(pk=data["event"])

        return data
