from django.db import models


class OTTPlatform(models.Model):
    name = models.CharField(max_length=100)
    website = models.URLField(blank=True)
    logo = models.ImageField(upload_to='ott_logos/', blank=True)

    def __str__(self):
        return self.name


class Movie(models.Model):

    RELEASE_TYPE_CHOICES = [
        ('THEATRE', 'Theatre'),
        ('OTT', 'OTT'),
        ('BOTH', 'Theatre + OTT'),
    ]

    title = models.CharField(max_length=200)
    synopsis = models.TextField()
    poster = models.ImageField(upload_to='posters/')

    release_date = models.DateField()
    release_type = models.CharField(
        max_length=10,
        choices=RELEASE_TYPE_CHOICES
    )

    languages = models.CharField(
        max_length=200,
        help_text="Comma separated (Hindi, Tamil, Telugu)"
    )

    genres = models.CharField(
        max_length=200,
        help_text="Comma separated (Action, Drama)"
    )

    cast = models.TextField(
        help_text="Main cast names"
    )

    theatre_booking_link = models.URLField(blank=True)

    ott_platform = models.ForeignKey(
        OTTPlatform,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    ott_watch_link = models.URLField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
