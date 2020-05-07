from unittest.mock import patch, Mock

from django.http import HttpResponse
from django.test import TestCase, Client
from django.urls import reverse

from tests.videodinges import factories
from videodinges import models


class IndexTestCase(TestCase):
	def setUp(self):
		self.client = Client()

	#@patch('videodinges.views.render')
	def test_index(self):

		#render.return_value = HttpResponse(b'data', status=200)

		video1 = factories.create(models.Video, title='Vid 1', slug='vid-1')
		video2 = factories.create(models.Video, title='Vid 2', slug='vid-2')
		resp = self.client.get(reverse('index'))
		self.assertEqual(resp.status_code, 200)
		self.assertContains(resp, 'Vid 1')
		self.assertContains(resp, 'vid-1.html')

		self.assertContains(resp, 'Vid 2')
		self.assertContains(resp, 'vid-2.html')
