from rest_framework import serializers
from .models import Movie, OTTPlatform


class OTTPlatformSerializer(serializers.ModelSerializer):
    class Meta:
        model = OTTPlatform
        fields = ['id', 'name', 'website', 'logo']


class MovieSerializer(serializers.ModelSerializer):
    ott_platform = OTTPlatformSerializer(read_only=True)
    poster = serializers.ImageField(use_url=True)

    class Meta:
        model = Movie
        fields = [
            'id',
            'title',
            'synopsis',
            'poster',
            'release_date',
            'release_type',
            'languages',
            'genres',
            'cast',
            'theatre_booking_link',
            'ott_platform',
            'ott_watch_link',
        ]
