from rest_framework import serializers
from .models import Movie, OTTPlatform


class OTTPlatformSerializer(serializers.ModelSerializer):
    logo = serializers.CharField(source='logo.url', read_only=True)

    class Meta:
        model = OTTPlatform
        fields = ['id', 'name', 'website', 'logo']


class MovieSerializer(serializers.ModelSerializer):
    poster = serializers.CharField(source='poster.url', read_only=True)
    ott_platform = OTTPlatformSerializer(read_only=True)

    class Meta:
        model = Movie
        fields = '__all__'
