from django.test import TestCase
from videodinges.models import Upload
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings

import tempfile

@override_settings(MEDIA_ROOT=tempfile.mkdtemp())
class UploadTestCase(TestCase):
	def setUp(self):
		Upload.objects.create(file=SimpleUploadedFile('some_file.txt', b'some contents'))

	def test_model_is_created(self):
		upload = Upload.objects.all()[0]
		self.assertEqual(upload.file.name, 'some_file.txt')
