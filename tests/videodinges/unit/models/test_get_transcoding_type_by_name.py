from django.test import SimpleTestCase
from videodinges.models import get_transcoding_type_by_name

class GetTranscodingTypeByNameTestCase(SimpleTestCase):

	def test_returns_transcoding_type_if_listed(self):
		result = get_transcoding_type_by_name('video/webm; codecs="vp9, opus"')
		self.assertEqual(result.name, 'video/webm; codecs="vp9, opus"')
		self.assertEqual(result.short_name, 'vp9')
		self.assertEqual(result.description, 'WebM with VP9 and Opus')
		self.assertEqual(result.priority, 100)

	def test_returns_none_if_not_listed(self):
		result = get_transcoding_type_by_name('non-existent')
		self.assertIsNone(result)
