import tempfile
from unittest import TestCase

from django.test import override_settings


class UploadMixin(TestCase):
	clean_uploads_after_run = True
	base_upload_dir: tempfile.TemporaryDirectory

	@classmethod
	def setUpClass(cls) -> None:
		super().setUpClass()
		cls.base_upload_dir = tempfile.TemporaryDirectory(suffix='-videodinges-tests')

	def setUp(self) -> None:
		super().setUp()
		self.media_root = tempfile.TemporaryDirectory(suffix='-' + self.__class__.__name__, dir=self.base_upload_dir.name)
		self.media_root_override_settings = override_settings(MEDIA_ROOT=self.media_root.name)
		self.media_root_override_settings.enable()

	def tearDown(self) -> None:
		self.media_root_override_settings.disable()
		if self.clean_uploads_after_run:
			self.media_root.cleanup()
		super().tearDown()

	@classmethod
	def tearDownClass(cls) -> None:
		if cls.clean_uploads_after_run:
			cls.base_upload_dir.cleanup()
		super().tearDownClass()
