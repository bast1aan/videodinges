from typing import List

from django.http import HttpResponse, HttpRequest

from . import models

__all__ = ['index']

def index(request: HttpRequest) -> HttpResponse:
	videos = models.Video.objects.all()
	if videos.count() == 0:
		video = models.Video(
			title='Test',
			slug='test',
			description='Test object',
		)
		video.save()
	else:
		video = videos[0]

	if video.transcodings.count() == 0:
		transcoding = models.Transcoding(video=video, quality='360p', file='somefile')
		transcoding.save()
	#transcodings: List[models.Transcoding] = video.transcodings.objects.all()

	videos_html = []
	for video in videos:
		videos_html.append(
			'<li>{title}: {transcodings}</li>'.format(
				title=video.title,
				transcodings=', '.join(tr.quality_obj.name for tr in video.transcodings.all()),
			)
		)


	return HttpResponse('<h1>Index!</h1>\n<ul>{videos}</ul>'.format(videos='\n'.join(videos_html)))