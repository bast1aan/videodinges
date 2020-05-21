from django.test import TestCase
from videodinges.models import Video
from datetime import datetime

class VideoTestCase(TestCase):
	def setUp(self):
		Video.objects.create(title='Title', slug='slug', description='Description')
	
	def test_model_is_created(self):
		video = Video.objects.get(slug='slug')
		self.assertEqual(video.slug, 'slug')
		self.assertEqual(video.title, 'Title')
		self.assertEqual(video.description, 'Description')
		self.assertIsInstance(video.created_at, datetime)
		self.assertIsInstance(video.updated_at, datetime)
