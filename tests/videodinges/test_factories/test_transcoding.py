import os

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from videodinges.models import Transcoding, Video, Upload
from tests.videodinges import factories, UploadMixin

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

	def test_does_not_create_video_when_providing_one(self):
		transcoding = factories.create(
			Transcoding,
			quality='720p',
			type='video/mp4',
			url='http://another_url',
			video=factories.create(Video, slug='yet-another-video-slug')
		)

		self.assertEquals(Video.objects.all().count(), 1)


class TranscodingWithUploadTestCase(UploadMixin, TestCase):
	def test_can_assign_upload(self):
		transcoding = factories.create(
			Transcoding,
			quality='720p',
			type='video/mp4',
			video=factories.create(Video, slug='yet-another-video-slug'),
			upload=factories.create(Upload, file=SimpleUploadedFile('my_upload.txt', b'some_contents'))
		)

		self.assertTrue(os.path.exists(os.path.join(self.media_root.name, 'my_upload.txt')))
		with open(os.path.join(self.media_root.name, 'my_upload.txt'), 'rb') as f:
			self.assertEquals(f.read(), b'some_contents')

