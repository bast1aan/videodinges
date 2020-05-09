from datetime import datetime
from typing import overload, Type, TypeVar

from django.core.files import File

from videodinges import models

import django.db.models

@overload
def create(
		model:Type[models.Transcoding],
		pk:int=None,
		id:int=None,
		video:models.Video=None,
		quality:str=None,
		type:str=None,
		upload:models.Upload=None,
		url:str=None
	) -> models.Transcoding: ...

@overload
def create(
		model:Type[models.Video],
		pk:int=None,
		id:int=None,
		title:str=None,
		slug:str=None,
		description:str=None,
		poster:models.Upload=None,
		og_image:models.Upload=None,
		default_quality:str=None,
		create_at:datetime=None,
		updated_at:datetime=None,
	) -> models.Video: ...

@overload
def create(
		model:Type[models.Upload],
		pk:int=None,
		id:int=None,
		file:File=None,
	) -> models.Upload: ...

T = TypeVar('T', bound=django.db.models.Model)

def create(model: Type[T], **kwargs) -> T: ...