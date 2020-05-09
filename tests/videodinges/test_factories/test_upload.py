from django.test import TestCase

from tests.videodinges import factories, UploadMixin
from videodinges.models import Upload

class UploadTestCase(UploadMixin, TestCase):
	def test_model_is_created(self):
		upload = factories.create(Upload)
		self.assertEqual(upload.file.name, 'some_file.txt')
