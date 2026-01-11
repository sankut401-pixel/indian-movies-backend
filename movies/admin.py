from django.contrib import admin
from .models import Movie, OTTPlatform


@admin.register(OTTPlatform)
class OTTPlatformAdmin(admin.ModelAdmin):
    list_display = ("name", "website")
    search_fields = ("name",)


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ("title", "release_type", "release_date", "created_at")
    list_filter = ("release_type", "release_date")
    search_fields = ("title", "languages", "genres", "cast")