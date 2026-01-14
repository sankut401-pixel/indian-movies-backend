from rest_framework import serializers
from .models import Movie, OTTPlatform
import cloudinary.utils


class OTTPlatformSerializer(serializers.ModelSerializer):
    logo = serializers.SerializerMethodField()

    class Meta:
        model = OTTPlatform
        fields = ["id", "name", "website", "logo"]

    def get_logo(self, obj):
        if not obj.logo:
            return ""
        url, _ = cloudinary.utils.cloudinary_url(
            obj.logo.public_id,
            secure=True
        )
        return url


class MovieSerializer(serializers.ModelSerializer):
    poster = serializers.SerializerMethodField()
    ott_platform = OTTPlatformSerializer(read_only=True)

    class Meta:
        model = Movie
        fields = "__all__"

    def get_poster(self, obj):
        if not obj.poster:
            return ""
        url, _ = cloudinary.utils.cloudinary_url(
            obj.poster.public_id,
            secure=True
        )
        return url
