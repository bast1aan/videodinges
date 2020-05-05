import os
from datetime import datetime
from typing import NamedTuple, Optional, Union

from django.db import models
from django.db.models import constraints
from django.db.models.query_utils import Q

class Quality(NamedTuple):
	name: str
	width: int
	height: int
	priority: int

class TranscodingType(NamedTuple):
	name: str
	short_name: str

	def __str__(self):
		return self.name

qualities = (
    Quality(name='360p', width=640, height=360, priority=1),
    Quality(name='480p', width=853, height=480, priority=2),
    Quality(name='720p', width=1280, height=720, priority=2),
    Quality(name='1080p', width=1920, height=1080, priority=1),
)

transcoding_types = (
	TranscodingType(name='video/webm', short_name='vp8'),
	TranscodingType(name='video/webm; codecs="vp8, vorbis"', short_name='vp8'),
	TranscodingType(name='video/webm; codecs="vp9, opus"', short_name='vp9'),
	TranscodingType(name='video/mp4', short_name='h.264'),
	TranscodingType(name='video/mp4; codecs="avc1.64001f,mp4a.40.2"', short_name='h.264'),
)

class Upload(models.Model):
	id = models.AutoField(primary_key=True)
	file = models.FileField()

	def __str__(self):
		return os.path.basename(self.file.path)

class Video(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=256)
    slug = models.CharField(max_length=256, unique=True)
    description = models.TextField()
    poster = models.OneToOneField(Upload, on_delete=models.PROTECT, blank=True, null=True, related_name='video_poster')
    og_image = models.OneToOneField(Upload, on_delete=models.PROTECT, blank=True, null=True, related_name='video_og_image')
    created_at = models.DateTimeField(default=datetime.now)
    updated_at = models.DateTimeField(default=datetime.now)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.updated_at = datetime.now()
        super().save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return self.title

    class Meta:
        indexes = [models.Index(fields=['slug'])]

class Transcoding(models.Model):
    id = models.AutoField(primary_key=True)
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='transcodings')
    quality = models.CharField(choices=((quality.name, quality.name) for quality in qualities), max_length=128)
    type = models.CharField(choices=((str(type_), str(type_)) for type_ in transcoding_types), max_length=128)
    upload = models.OneToOneField(Upload, on_delete=models.PROTECT, blank=True, null=True)
    url = models.CharField(max_length=256, null=True, blank=True, unique=True)

    def __str__(self):
        return self.quality

    @property
    def quality_obj(self):
        return get_quality_by_name(self.quality)

    class Meta:
        unique_together = ('video', 'quality', 'type')
        constraints = [constraints.CheckConstraint(check=Q(upload__isnull=False) | Q(url__isnull=False),
                                                   name='upload_or_url_is_filled'),
                       constraints.CheckConstraint(check=~(Q(upload__isnull=False) & Q(url__isnull=False)),
                                                   name='upload_and_url_cannot_both_be_filled'),
                      ]

def get_quality_by_name(name: str) -> Optional[Quality]:
	for quality in qualities:
		if quality.name == name:
			return quality

def get_short_name_of_transcoding_type(transcoding_type: Union[str, TranscodingType]) -> str:
	if isinstance(transcoding_type, str):
		for type_ in transcoding_types:
			if type_.name == transcoding_type:
				transcoding_type = type_

	if isinstance(transcoding_type, TranscodingType):
		return transcoding_type.short_name