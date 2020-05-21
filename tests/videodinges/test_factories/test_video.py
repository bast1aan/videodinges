from django.test import TestCase
from videodinges.models import Video
from tests.videodinges import factories
from datetime import datetime

class VideoTestCase(TestCase):
	def test_factory_returns_model(self):
		video = factories.create(Video)
		self.assertEqual(video.slug, 'slug-1')
		self.assertEqual(video.title, 'Title 1')
		self.assertEqual(video.description, 'Description 1')
		self.assertIsInstance(video.created_at, datetime)
		self.assertIsInstance(video.updated_at, datetime)

	def test_factory_can_create_multiple_models(self):
		video1 = factories.create(Video)
		video2 = factories.create(Video)
		video3 = factories.create(Video)

		self.assertEqual(video1.slug, 'slug-1')
		self.assertEqual(video1.title, 'Title 1')
		self.assertEqual(video1.description, 'Description 1')
		self.assertIsInstance(video1.created_at, datetime)
		self.assertIsInstance(video1.updated_at, datetime)

		self.assertEqual(video2.slug, 'slug-2')
		self.assertEqual(video2.title, 'Title 2')
		self.assertEqual(video2.description, 'Description 2')
		self.assertIsInstance(video2.created_at, datetime)
		self.assertIsInstance(video2.updated_at, datetime)

		self.assertEqual(video3.slug, 'slug-3')
		self.assertEqual(video3.title, 'Title 3')
		self.assertEqual(video3.description, 'Description 3')
		self.assertIsInstance(video3.created_at, datetime)
		self.assertIsInstance(video3.updated_at, datetime)

	def test_factory_runs_only_2_queries(self):
		""" Factory should only use 2 queries: one for selecting primary key, and one for inserting record """
		with self.assertNumQueries(2):
			video = factories.create(Video)
