""" Test video page """
from django.http import HttpResponse
from django.test import TestCase, Client
from django.urls import reverse

from tests.videodinges import factories
from videodinges import models


class VideoTestCase(TestCase):
	def setUp(self):
		self.client = Client()

	def test_video(self):

		video = factories.create(
			models.Video,
			title='Vid 1',
			slug='vid-1',
		)
		transcoding1 = factories.create(
			models.Transcoding,
			video=video,
			quality='480p',
			type='video/webm',
			url='http://480p.webm',
		)
		transcoding2 = factories.create(
			models.Transcoding,
			video=video,
			quality='480p',
			type='video/mp4',
			url='http://480p.mp4',
		)
		transcoding3 = factories.create(
			models.Transcoding,
			video=video,
			quality='720p',
			type='video/webm',
			url='http://720p.webm',
		)
		transcoding4 = factories.create(
			models.Transcoding,
			video=video,
			quality='720p',
			type='video/mp4',
			url='http://720p.mp4',
		)

		resp:HttpResponse = self.client.get(reverse('video', args=['vid-1']))
		content:str = resp.content.decode(resp.charset)
		# TODO: parse HTML, check for essential elements
		self.assertEqual(resp.status_code, 200)
		self.assertContains(resp, 'Vid 1')
		#self.assertContains(resp, '')
		#self.assertRegexpMatches(resp.content)

		#self.assertContains(resp, 'Vid 2')
		#self.assertContains(resp, 'vid-2.html')
