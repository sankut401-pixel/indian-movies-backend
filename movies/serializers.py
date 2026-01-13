from rest_framework import serializers
from .models import Movie, OTTPlatform


class OTTPlatformSerializer(serializers.ModelSerializer):
    logo = serializers.SerializerMethodField()

    class Meta:
        model = OTTPlatform
        fields = ['id', 'name', 'website', 'logo']

    def get_logo(self, obj):
        try:
            if obj.logo and hasattr(obj.logo, "url"):
                url = obj.logo.url
                # force https (Cloudinary sometimes gives http)
                return url.replace("http://", "https://")
        except Exception:
            pass
        return ""



class MovieSerializer(serializers.ModelSerializer):
    poster = serializers.SerializerMethodField()
    ott_platform = OTTPlatformSerializer(read_only=True)

    class Meta:
        model = Movie
        fields = "__all__"

    def get_poster(self, obj):
        try:
            if obj.poster and hasattr(obj.poster, "url"):
                return obj.poster.url.replace("http://", "https://")
        except Exception:
            pass
        return ""

