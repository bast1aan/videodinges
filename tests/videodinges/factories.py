""" Module generating useful models in 1 place """
import tempfile
from typing import Type, TypeVar

from django.core.files.uploadedfile import SimpleUploadedFile
import django.db.models
from django.test import override_settings

from videodinges import models

T = TypeVar('T', bound=django.db.models.Model)


def create(model: Type[T], **kwargs) -> T:
	if model is models.Video:
		return models.Video.objects.create(**{**dict(title='Title', slug='slug', description='Description'), **kwargs})

	if model is models.Transcoding:
		video = create(models.Video, title='Title', slug='slug', description='Description') \
			if 'video' not in kwargs else None
		defaults = dict(
			video=video,
			quality=models.qualities[0].name,
			type=str(models.transcoding_types[0]),
		)
		if 'upload' not in kwargs:
			# only URL if no upload for they are multually exclusive
			defaults['url'] = 'https://some_url'

		return models.Transcoding.objects.create(**{**defaults, **kwargs})

	if model is models.Upload:
		return _upload(**kwargs)

@override_settings(MEDIA_ROOT=tempfile.mkdtemp())
def _upload(**kwargs):
	file = SimpleUploadedFile('some_file.txt', b'some contents') \
		if 'file' not in kwargs else None
	return models.Upload.objects.create(**{**dict(file=file), **kwargs})


# TODO fix annoying dict notation to something more gentle.
