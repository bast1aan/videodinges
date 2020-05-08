""" Test video page """
from django.http import HttpResponse
from django.test import TestCase, Client
from django.urls import reverse

from tests.videodinges import factories
from videodinges import models


class VideoTestCase(TestCase):
	def setUp(self):
		self.client = Client()

	def test_video_view_renders_properly(self):

		video = factories.create(
			models.Video,
			title='Vid 1',
			slug='vid-1',
			default_quality='480p',
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

		self.assertEqual(resp.status_code, 200)

		content:str = resp.content.decode(resp.charset)

		srctag = '<source src="{url}" type="{type}" />'

		self.assertInHTML(
			srctag.format(url=transcoding1.url, type=transcoding1.type),
			content,
		)
		self.assertInHTML(
			srctag.format(url=transcoding2.url, type=transcoding2.type),
			content
		)
		self.assertInHTML(
			srctag.format(url=transcoding3.url, type=transcoding3.type),
			content,
			count=0
		)
		self.assertInHTML(
			srctag.format(url=transcoding4.url, type=transcoding4.type),
			content,
			count=0
		)

		self.assertInHTML('<title>Vid 1</title>', content)

		self.assertInHTML('<h1>Vid 1</h1>', content)

		self.assertInHTML('<p>Description</p>', content)

		self.assertInHTML('<strong>480p versie</strong>', content)

		self.assertInHTML(
			'<a href="vid-1.html?quality=720p" onclick="vidTimeInUrl(this);">720p versie</a>',
			content
		)

		self.assertIn(
			'You need a browser that understands HTML5 video and supports h.264 or vp8 codecs.',
			content
		)

		self.assertInHTML(
			'<script src="static/js/video.js" type="text/javascript"></script>',
			content
		)

	def test_video_show_correct_default_quality(self):

		video = factories.create(
			models.Video,
			title='Vid 1',
			slug='vid-1',
			default_quality='720p',
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

		self.assertEqual(resp.status_code, 200)

		content:str = resp.content.decode(resp.charset)

		srctag = '<source src="{url}" type="{type}" />'

		self.assertInHTML(
			srctag.format(url=transcoding1.url, type=transcoding1.type),
			content,
			count=0
		)
		self.assertInHTML(
			srctag.format(url=transcoding2.url, type=transcoding2.type),
			content,
			count=0
		)
		self.assertInHTML(
			srctag.format(url=transcoding3.url, type=transcoding3.type),
			content,
		)
		self.assertInHTML(
			srctag.format(url=transcoding4.url, type=transcoding4.type),
			content,
		)

		self.assertInHTML(
			'<a href="vid-1.html?quality=480p" onclick="vidTimeInUrl(this);">480p versie</a>',
			content
		)

		self.assertInHTML('<strong>720p versie</strong>', content)


	def test_video_shows_correct_quality_for_parameter(self):

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

		resp:HttpResponse = self.client.get(
			reverse('video', args=['vid-1']) + '?quality=720p')

		self.assertEqual(resp.status_code, 200)

		content:str = resp.content.decode(resp.charset)

		srctag = '<source src="{url}" type="{type}" />'

		self.assertInHTML(
			srctag.format(url=transcoding1.url, type=transcoding1.type),
			content,
			count=0
		)
		self.assertInHTML(
			srctag.format(url=transcoding2.url, type=transcoding2.type),
			content,
			count=0
		)
		self.assertInHTML(
			srctag.format(url=transcoding3.url, type=transcoding3.type),
			content,
		)
		self.assertInHTML(
			srctag.format(url=transcoding4.url, type=transcoding4.type),
			content,
		)
