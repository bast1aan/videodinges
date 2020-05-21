from django.db import models

from tests.videodinges import factories
from django.test import TestCase

class CreateTestCase(TestCase):

	def test_factory_returns_model(self):

		class NotImplementedModel(models.Model):
			class Meta:
				app_label = 'some_test_label'

		with self.assertRaises(NotImplementedError):
			factories.create(NotImplementedModel)

