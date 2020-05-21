""" Module generating useful models in 1 place """
from typing import Type, TypeVar

from django.core.files.uploadedfile import SimpleUploadedFile
import django.db.models

from videodinges import models

T = TypeVar('T', bound=django.db.models.Model)


def create(model: Type[T], **kwargs) -> T:
	if model is models.Video:
		return _create_with_defaults(models.Video, kwargs, title='Title', slug='slug', description='Description')

	if model is models.Transcoding:
		defaults = dict(
			video=lambda: create(models.Video),
			quality=models.qualities[0].name,
			type=str(models.transcoding_types[0]),
		)
		if 'upload' not in kwargs:
			# only URL if no upload for they are multually exclusive
			defaults['url'] = 'https://some_url'

		return _create_with_defaults(models.Transcoding, kwargs, **defaults)

	if model is models.Upload:
		return _create_with_defaults(models.Upload, kwargs, file=SimpleUploadedFile('some_file.txt', b'some contents'))


def _create_with_defaults(model: Type[T], kwargs: dict, **defaults) -> T:
	"""
		Return created django model instance.
		When providing lambda as default item, the result of the lambda will be taken.
		The lambda will ONLY be executed when not provided in kwargs.

		:param model: django model to create
		:param kwargs: keyword arguments to fill the model
		:param defaults: default keyword arguments to use when not mentioned in kwargs
	"""

	for k, v in defaults.items():
		if callable(v) and not k in kwargs:
			defaults[k] = v()

	return model.objects.create(**{**defaults, **kwargs})
