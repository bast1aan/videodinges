from django.test import TestCase
from videodinges.models import TranscodingType, get_short_name_of_transcoding_type

class GetShortNameOfTranscodingTypeTestCase(TestCase):

	def test_gets_transcoding_by_name(self):
		result = get_short_name_of_transcoding_type('video/webm; codecs="vp8, vorbis"')
		self.assertEqual(result, 'vp8')

	def test_gets_transcoding_by_transcoding_object(self):
		result = get_short_name_of_transcoding_type(TranscodingType(name='Looooong naaaaame', short_name='shrt nm'))
		self.assertEqual(result, 'shrt nm')