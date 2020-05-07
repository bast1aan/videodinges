from django.test import TestCase
from videodinges.models import Transcoding
from tests.videodinges import factories
from datetime import datetime

class TranscodingTestCase(TestCase):
	def test_factory_returns_model(self):
		transcoding = factories.create(Transcoding)
		self.assertEqual(transcoding.video.slug, 'slug')
		self.assertEqual(transcoding.quality, '360p')
		self.assertEqual(transcoding.type, 'video/webm')
		self.assertEqual(transcoding.url, 'https://some_url')
