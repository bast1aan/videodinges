from django.test import TestCase
from videodinges.models import Transcoding, Video
from tests.videodinges import factories
from datetime import datetime

class TranscodingTestCase(TestCase):
	def test_factory_returns_model(self):
		transcoding = factories.create(Transcoding)
		self.assertEqual(transcoding.video.slug, 'slug')
		self.assertEqual(transcoding.quality, '360p')
		self.assertEqual(transcoding.type, 'video/webm')
		self.assertEqual(transcoding.url, 'https://some_url')

	def test_can_overwrite_kwargs(self):
		transcoding = factories.create(
			Transcoding,
			quality='720p',
			type='video/mp4',
			url='http://another_url',
			video=factories.create(Video, slug='yet-another-video-slug')
		)

		self.assertEqual(transcoding.video.slug, 'yet-another-video-slug')
		self.assertEqual(transcoding.quality, '720p')
		self.assertEqual(transcoding.type, 'video/mp4')
		self.assertEqual(transcoding.url, 'http://another_url')
