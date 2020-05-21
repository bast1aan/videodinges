from django.test import TestCase
from videodinges.models import Video
from tests.videodinges import factories
from datetime import datetime

class VideoTestCase(TestCase):
	def test_factory_returns_model(self):
		video = factories.create(Video)
		self.assertEqual(video.slug, 'slug')
		self.assertEqual(video.title, 'Title')
		self.assertEqual(video.description, 'Description')
		self.assertIsInstance(video.created_at, datetime)
		self.assertIsInstance(video.updated_at, datetime)
