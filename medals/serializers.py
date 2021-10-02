from rest_framework import serializers

from .models import Medal


class MedalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medal
        fields = "__all__"
