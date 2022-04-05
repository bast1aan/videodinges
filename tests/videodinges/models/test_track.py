from django.db.utils import IntegrityError

from django.test import TestCase

from tests.videodinges import factories, UploadMixin
from videodinges.models import Track, Video, Upload


class TrackTestCase(UploadMixin, TestCase):
	def setUp(self):
		super().setUp()
		self.video = Video.objects.create(title='Title', slug='slug', description='Description')

	def test_model_is_created_with_required_fields(self):
		Track.objects.create(video=self.video, lang='en', upload=factories.create(Upload))
		track = Track.objects.all()[0]
		self.assertEqual(track.video.slug, 'slug')
		self.assertEqual(track.default, False)
		self.assertEqual(track.kind, 'subtitles')
		self.assertEqual(track.lang, 'en')
		self.assertEqual(track.label, None)
		self.assertEqual(track.upload.file.name, 'some_file.txt')

	def test_model_is_created_with_nonrequired_fields(self):
		Track.objects.create(
			video=self.video,
			lang='en',
			upload=factories.create(Upload),
			default=True,
			label='Something',
			kind='chapters',
		)
		track = Track.objects.all()[0]
		self.assertEqual(track.video.slug, 'slug')
		self.assertEqual(track.default, True)
		self.assertEqual(track.kind, 'chapters')
		self.assertEqual(track.lang, 'en')
		self.assertEqual(track.label, 'Something')
		self.assertEqual(track.upload.file.name, 'some_file.txt')

	def test_can_create_two_models(self):
		model1 = Track.objects.create(video=self.video, lang='en', upload=factories.create(Upload))
		model2 = Track.objects.create(video=self.video, lang='nl', upload=factories.create(Upload))
		self.assertEqual({model1, model2}, set((m for m in Track.objects.all())))

		self.assertEqual(model1.video, self.video)
		self.assertEqual(model1.default, False)
		self.assertEqual(model1.kind, 'subtitles')
		self.assertEqual(model1.lang, 'en')

		self.assertEqual(model2.video, self.video)
		self.assertEqual(model2.default, False)
		self.assertEqual(model2.kind, 'subtitles')
		self.assertEqual(model2.lang, 'nl')

	def test_can_create_two_models_with_one_default(self):
		model1 = Track.objects.create(video=self.video, default=True, lang='en', upload=factories.create(Upload))
		model2 = Track.objects.create(video=self.video, lang='nl', upload=factories.create(Upload))
		self.assertEqual({model1, model2}, set((m for m in Track.objects.all())))

		self.assertEqual(model1.video, self.video)
		self.assertEqual(model1.default, True)
		self.assertEqual(model1.kind, 'subtitles')
		self.assertEqual(model1.lang, 'en')

		self.assertEqual(model2.video, self.video)
		self.assertEqual(model2.default, False)
		self.assertEqual(model2.kind, 'subtitles')
		self.assertEqual(model2.lang, 'nl')

	def test_cannot_set_default_twice(self):
		video = factories.create(Video)
		Track.objects.create(video=video, default=True, lang='en', upload=factories.create(Upload))
		with self.assertRaisesMessage(IntegrityError, 'UNIQUE constraint failed: tracks.video_id'):
			Track.objects.create(video=video, default=True, lang='nl', upload=factories.create(Upload))

	def test_cannot_set_two_subtitles_with_same_lang(self):
		video = factories.create(Video)
		Track.objects.create(video=video, lang='en', upload=factories.create(Upload))
		with self.assertRaisesMessage(IntegrityError, 'UNIQUE constraint failed: tracks.video_id'):
			Track.objects.create(video=video, lang='en', upload=factories.create(Upload))

	def test_can_create_two_models_with_same_lang_but_different_kind(self):
		model1 = Track.objects.create(video=self.video, lang='en', upload=factories.create(Upload))
		model2 = Track.objects.create(video=self.video, lang='en', kind='chapters', upload=factories.create(Upload))
		self.assertEqual({model1, model2}, set((m for m in Track.objects.all())))

		self.assertEqual(model1.video, self.video)
		self.assertEqual(model1.default, False)
		self.assertEqual(model1.kind, 'subtitles')
		self.assertEqual(model1.lang, 'en')

		self.assertEqual(model2.video, self.video)
		self.assertEqual(model2.default, False)
		self.assertEqual(model2.kind, 'chapters')
		self.assertEqual(model2.lang, 'en')
