from django.contrib import admin
from .models import Movie, OTTPlatform


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'release_date', 'release_type')
    list_filter = ('release_type', 'release_date')
    search_fields = ('title', 'languages', 'genres')


@admin.register(OTTPlatform)
class OTTPlatformAdmin(admin.ModelAdmin):
    search_fields = ('name',)
