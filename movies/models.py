from django.db import models


class OTTPlatform(models.Model):
    name = models.CharField(max_length=100)
    website = models.URLField(blank=True)
    logo = models.URLField(blank=True)   # ✅ URL ONLY

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

    poster = models.URLField(blank=True)  # ✅ URL ONLY

    release_date = models.DateField()
    release_type = models.CharField(max_length=10, choices=RELEASE_TYPE_CHOICES)

    rating = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        null=True,
        blank=True
    )

    languages = models.CharField(max_length=200)
    genres = models.CharField(max_length=200)
    cast = models.TextField()

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
