from django.test import TestCase
from videodinges.models import Transcoding, Video, qualities, transcoding_types

class TranscodingTestCase(TestCase):
	def setUp(self):
		video = Video.objects.create(title='Title', slug='slug', description='Description')
		Transcoding.objects.create(video=video, quality=qualities[0].name, type=str(transcoding_types[0]), url='https://some_url')

	def test_model_is_created(self):
		transcoding = Transcoding.objects.all()[0]
		self.assertEqual(transcoding.video.slug, 'slug')
		self.assertEqual(transcoding.quality, '360p')
		self.assertEqual(transcoding.type, 'video/webm')
		self.assertEqual(transcoding.url, 'https://some_url')
