from django.test import TestCase

from tests.videodinges import UploadMixin
from videodinges.models import Upload
from django.core.files.uploadedfile import SimpleUploadedFile


class UploadTestCase(UploadMixin, TestCase):
	def setUp(self):
		super().setUp()
		Upload.objects.create(file=SimpleUploadedFile('some_file.txt', b'some contents'))

	def test_model_is_created(self):
		upload = Upload.objects.all()[0]
		self.assertEqual(upload.file.name, 'some_file.txt')
