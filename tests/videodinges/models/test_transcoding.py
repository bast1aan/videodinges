from django.db.utils import IntegrityError

from django.test import TestCase

from tests.videodinges import factories
from videodinges.models import Transcoding, Video, qualities, transcoding_types, Upload


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


class CreateTranscodingTestCase(TestCase):

	def test_upload_and_url_cannot_both_be_filled(self):
		video = factories.create(Video)
		with self.assertRaisesMessage(IntegrityError, 'CHECK constraint failed: upload_and_url_cannot_both_be_filled'):
			Transcoding.objects.create(
				video=video,
				quality=qualities[0].name,
				type=str(transcoding_types[0]),
				url='https://some_url',
				upload=factories.create(Upload)
			)

	def test_either_upload_or_url_must_be_filled(self):
		video = factories.create(Video)

		with self.assertRaisesMessage(IntegrityError, 'CHECK constraint failed: upload_or_url_is_filled'):
			Transcoding.objects.create(
				video=video,
				quality=qualities[0].name,
				type=str(transcoding_types[0]),
			)

	def test_no_duplicate_qualities_for_same_video_and_type_can_be_created(self):
		video = factories.create(Video)

		Transcoding.objects.create(
			video=video,
			quality=qualities[0].name,
			type=str(transcoding_types[0]),
			url='https://some_url',
		)

		with self.assertRaisesMessage(IntegrityError, 'UNIQUE constraint failed: transcodings.video_id, transcodings.quality, transcodings.type'):
			Transcoding.objects.create(
				video=video,
				quality=qualities[0].name,
				type=str(transcoding_types[0]),
				url='https://some_url',
			)
