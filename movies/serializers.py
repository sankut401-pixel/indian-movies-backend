from rest_framework import serializers
from .models import Movie, OTTPlatform


class OTTPlatformSerializer(serializers.ModelSerializer):
    class Meta:
        model = OTTPlatform
        fields = ['id', 'name', 'website', 'logo']


class MovieSerializer(serializers.ModelSerializer):
    poster = serializers.SerializerMethodField()
    ott_platform = OTTPlatformSerializer(read_only=True)

    class Meta:
        model = Movie
        fields = "__all__"

    def get_poster(self, obj):
        try:
            if obj.poster and hasattr(obj.poster, "url"):
                url = obj.poster.url
                # Force HTTPS for Android APK
                if url.startswith("http://"):
                    url = url.replace("http://", "https://")
                return url
            return ""
        except Exception:
            return ""
