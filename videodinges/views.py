from collections import defaultdict
from typing import List, Dict, Any

from django.http import HttpResponse, HttpRequest, Http404
from django.shortcuts import render
from . import models

def video(request: HttpRequest, slug: str) -> HttpResponse:
	try:
		video = models.Video.objects.get(slug=slug)
	except models.Video.DoesNotExist:
		raise Http404('Video not found')

	template_data = dict(
		og_image=video.og_image.file.url if video.og_image else None,
		title=video.title,
		poster=video.poster.file.url if video.poster else None,
		description=video.description,
		slug=video.slug
	)

	qualities = _get_qualities(video)
	try:
		quality = qualities[request.GET['quality']]
	except:
		quality = next(iter(qualities.values()))

	template_data.update(
		width=quality[0].quality_obj.width,
		height=quality[0].quality_obj.height,
	)

	template_data['sources'] = [
		{
			'src': _url_for(transcoding),
			'type': transcoding.type,
		}
			for transcoding in quality ]

	template_data['used_codecs'] = [
		models.get_short_name_of_transcoding_type(transcoding.type)
			for transcoding in quality
	]

	template_data['qualities'] = qualities.keys()

	return render(request, 'video.html.j2', template_data, using='jinja2')

def _get_dict_from_models_with_fields(model, *fields: str) -> Dict[str, Any]:
	ret = {}
	for field in fields:
		ret[field] = model.__dict__[field]
	return ret

def _get_qualities(video: models.Video) -> Dict[str, List[models.Transcoding]]:
	transcodings: List[models.Transcoding] = video.transcodings.order_by('quality').all()
	qualities = defaultdict(list)
	for transcoding in transcodings:
		qualities[transcoding.quality_obj.name].append(transcoding)
	return dict(qualities)

def _url_for(transcoding: models.Transcoding) -> str:
	if transcoding.url:
		return transcoding.url
	elif transcoding.upload:
		return transcoding.upload.file.url
