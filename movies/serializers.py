from rest_framework import serializers
from .models import Movie, OTTPlatform


class OTTPlatformSerializer(serializers.ModelSerializer):
    logo = serializers.SerializerMethodField()

    class Meta:
        model = OTTPlatform
        fields = ["id", "name", "website", "logo"]

    def get_logo(self, obj):
        if obj.logo:
            try:
                return obj.logo.url
            except Exception:
                return ""
        return ""


class MovieSerializer(serializers.ModelSerializer):
    poster = serializers.SerializerMethodField()
    ott_platform = OTTPlatformSerializer(read_only=True)

    class Meta:
        model = Movie
        fields = "__all__"

    def get_poster(self, obj):
        if obj.poster:
            try:
                return obj.poster.url
            except Exception:
                return ""
        return ""
