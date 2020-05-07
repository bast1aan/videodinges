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
		video = create(models.Video, title='Title', slug='slug', description='Description')
		return models.Transcoding.objects.create(
			**{
				**dict(
					video=video,
					quality=models.qualities[0].name,
					type=str(models.transcoding_types[0]),
					url='https://some_url',
				),
				**kwargs
			}
		)

	if model is models.Upload:
		return _upload(**kwargs)

@override_settings(MEDIA_ROOT=tempfile.mkdtemp())
def _upload(**kwargs):
	return models.Upload.objects.create(**{**dict(file=SimpleUploadedFile('some_file.txt', b'some contents')), **kwargs})


# TODO fix annoying dict notation to something more gentle.