import tempfile
from unittest import TestCase

from django.test import override_settings


class UploadMixin(TestCase):
	base_upload_dir: str
	@classmethod
	def setUpClass(cls) -> None:
		super().setUpClass()
		cls.base_upload_dir = tempfile.mkdtemp(suffix='-videodinges-tests')

	def setUp(self) -> None:
		super().setUp()
		media_root = tempfile.mkdtemp(suffix='-' + self.__class__.__name__, dir=self.base_upload_dir)
		self.media_root_override_settings = override_settings(MEDIA_ROOT=media_root)
		self.media_root_override_settings.enable()

	def tearDown(self) -> None:
		self.media_root_override_settings.disable()
		super().tearDown()
