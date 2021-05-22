from datetime import datetime
from django.db import models

# Create your models here.


class YVideoData(models.Model):
    id = models.CharField(primary_key=True, max_length=50)
    title = models.CharField(max_length=254)
    description = models.CharField(max_length=254, blank=True)
    publishing_datetime = models.DateTimeField(blank=True, default=datetime.now)
    thumbnail_url = models.CharField(max_length=254, null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'yvideo_data'
        indexes = [
            models.Index(fields=["title", "description"]),
            models.Index(
                fields=[
                    "-publishing_datetime",
                ]
            ),
        ]