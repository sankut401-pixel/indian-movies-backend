from rest_framework import serializers
from .models import Movie, OTTPlatform


class OTTPlatformSerializer(serializers.ModelSerializer):
    class Meta:
        model = OTTPlatform
        fields = ["id", "name", "website", "logo"]


class MovieSerializer(serializers.ModelSerializer):
    ott_platform = OTTPlatformSerializer(read_only=True)

    class Meta:
        model = Movie
        fields = "__all__"
