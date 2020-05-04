from datetime import datetime
from typing import NamedTuple

from django.db import models

class Quality(NamedTuple):
	name: str
	width: int
	height: int
	priority: int

qualities = (
    Quality(name='360p', width=640, height=360, priority=1),
    Quality(name='480p', width=853, height=480, priority=2),
    Quality(name='720p', width=1280, height=720, priority=2),
    Quality(name='1080p', width=1920, height=1080, priority=1),
)


class Video(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=256)
    slug = models.CharField(max_length=256)
    description = models.TextField()
    created_at = models.DateTimeField(default=datetime.now)
    updated_at = models.DateTimeField(default=datetime.now)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.updated_at = datetime.now()
        super().save(force_insert, force_update, using, update_fields)


class Transcoding(models.Model):
    id = models.AutoField(primary_key=True)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    quality = models.CharField(choices=((quality.name, quality.name) for quality in qualities), max_length=128)
    file = models.FileField()
