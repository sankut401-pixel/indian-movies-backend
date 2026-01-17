from django.core.management.base import BaseCommand
from movies.models import Movie, OTTPlatform

CLOUDINARY_BASE = "https://res.cloudinary.com/dqqexq1sy/image/upload/"

class Command(BaseCommand):
    help = "Fix old media paths to full Cloudinary URLs"

    def handle(self, *args, **kwargs):
        # Fix movie posters
        for movie in Movie.objects.all():
            if movie.poster and not movie.poster.startswith("http"):
                movie.poster = CLOUDINARY_BASE + movie.poster
                movie.save()
                self.stdout.write(f"Fixed poster for: {movie.title}")

        # Fix OTT logos
        for ott in OTTPlatform.objects.all():
            if ott.logo and not ott.logo.startswith("http"):
                ott.logo = CLOUDINARY_BASE + ott.logo
                ott.save()
                self.stdout.write(f"Fixed logo for: {ott.name}")

        self.stdout.write(self.style.SUCCESS("All media URLs fixed successfully"))
