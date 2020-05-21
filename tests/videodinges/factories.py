""" Module generating useful models in 1 place """
from inspect import signature
from typing import Type, TypeVar

from django.core.files.uploadedfile import SimpleUploadedFile
import django.db.models

from videodinges import models

T = TypeVar('T', bound=django.db.models.Model)


def create(model: Type[T], **kwargs) -> T:
	if model is models.Video:
		return _create_with_defaults(models.Video, kwargs,
			title=lambda x: 'Title {}'.format(x),
			slug=lambda x: 'slug-{}'.format(x),
			description=lambda x: 'Description {}'.format(x),
		)

	if model is models.Transcoding:
		def url():
			# only URL if no upload for they are mutually exclusive
			if 'upload' not in kwargs:
				return 'https://some_url'

		return _create_with_defaults(models.Transcoding, kwargs,
			video=lambda: create(models.Video),
			quality=models.qualities[0].name,
			type=str(models.transcoding_types[0]),
			url=url,
		)

	if model is models.Upload:
		return _create_with_defaults(models.Upload, kwargs, file=SimpleUploadedFile('some_file.txt', b'some contents'))

	raise NotImplementedError('Factory for %s not implemented' % model)


def _create_with_defaults(model: Type[T], kwargs: dict, **defaults) -> T:
	"""
		Return created django model instance.
		When providing lambda as default item, the result of the lambda will be taken.
		The lambda will ONLY be executed when not provided in kwargs.

		When a lambda requires an argument, the primary key of the to be created object
		will be provided to that argument. This is useful for generating unique fields.

		:param model: django model to create
		:param kwargs: keyword arguments to fill the model
		:param defaults: default keyword arguments to use when not mentioned in kwargs
	"""

	_next_pk = 0
	def next_pk():
		# Queries next pk only one time during creation
		nonlocal _next_pk
		if _next_pk == 0:
			_next_pk = _query_next_pk(model)
		return _next_pk

	for k, v in defaults.items():
		if callable(v) and not k in kwargs:
			if len(signature(v).parameters) == 1:
				result = v(next_pk())
			else:
				result = v()
			defaults[k] = result

	return model.objects.create(**{**defaults, **kwargs})


def _query_next_pk(model: Type[T]) -> int:
	try:
		return model.objects.order_by('-pk').first().pk + 1
	except AttributeError:
		return 1
