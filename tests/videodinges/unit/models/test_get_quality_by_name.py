from django.test import SimpleTestCase
from videodinges.models import get_quality_by_name

class GetQualityByNameTestCase(SimpleTestCase):

	def test_returns_quality_if_listed(self):
		result = get_quality_by_name('480p')
		self.assertEqual(result.name, '480p')
		self.assertEqual(result.width, 853)
		self.assertEqual(result.height, 480)
		self.assertEqual(result.priority, 2)

	def test_returns_none_if_not_listed(self):
		result = get_quality_by_name('non-existend')
		self.assertIsNone(result)
