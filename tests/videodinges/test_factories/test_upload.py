import os

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from tests.videodinges import factories, UploadMixin
from videodinges.models import Upload

class UploadTestCase(UploadMixin, TestCase):
	def test_model_is_created(self):
		upload = factories.create(Upload)
		self.assertEqual(upload.file.name, 'some_file.txt')
		self.assertTrue(os.path.exists(os.path.join(self.media_root.name, 'some_file.txt')))

	def test_upload_does_not_create_file_when_providing_upload(self):
		upload = factories.create(Upload, file=SimpleUploadedFile('my_file.txt', b'some contents'))
		self.assertEqual(upload.file.name, 'my_file.txt')
		self.assertFalse(os.path.exists(os.path.join(self.media_root.name, 'some_file.txt')))
		self.assertTrue(os.path.exists(os.path.join(self.media_root.name, 'my_file.txt')))
