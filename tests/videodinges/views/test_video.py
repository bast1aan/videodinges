""" Test video page """
from django.http import HttpResponse
from django.test import TestCase, Client
from django.urls import reverse

from tests.videodinges import factories, UploadMixin
from videodinges import models


class VideoTestCase(UploadMixin, TestCase):
	def setUp(self):
		super().setUp()
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
			type='video/webm; codecs="vp9, opus"',
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
			type='video/webm; codecs="vp9, opus"',
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
			"""<video width="853" height="480" controls="controls">
				<source src="http://480p.webm" type='video/webm; codecs="vp9, opus"' />
				<source src="http://480p.mp4" type='video/mp4' />
				You need a browser that understands HTML5 video and supports h.264 or vp9 codecs.
			</video>""",
			content,
		)

		self.assertInHTML('<title>Vid 1</title>', content)

		self.assertInHTML('<h1>Vid 1</h1>', content)

		self.assertInHTML('<p>Description 1</p>', content)

		self.assertInHTML('<strong>480p versie</strong>', content)

		self.assertInHTML(
			'<a href="vid-1.html?quality=720p" onclick="vidTimeInUrl(this);">720p versie</a>',
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
			type='video/webm; codecs="vp8, vorbis"',
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
			type='video/webm; codecs="vp8, vorbis"',
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

		self.assertInHTML(
			"""<video width="1280" height="720" controls="controls">
				<source src="http://720p.webm" type='video/webm; codecs="vp8, vorbis"' />
				<source src="http://720p.mp4" type='video/mp4' />
				You need a browser that understands HTML5 video and supports h.264 or vp8 codecs.
			</video>""",
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
			type='video/webm; codecs="vp8, vorbis"',
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
			type='video/webm; codecs="vp8, vorbis"',
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

		self.assertInHTML(
			"""<video width="1280" height="720" controls="controls">
				<source src="http://720p.webm" type='video/webm; codecs="vp8, vorbis"' />
				<source src="http://720p.mp4" type='video/mp4' />
				You need a browser that understands HTML5 video and supports h.264 or vp8 codecs.
			</video>""",
			content,
		)


		self.assertInHTML(
			'<a href="vid-1.html?quality=480p" onclick="vidTimeInUrl(this);">480p versie</a>',
			content
		)

		self.assertInHTML('<strong>720p versie</strong>', content)

	def test_video_uploads_shows_correctly(self):

		image = factories.create(models.Upload)
		movie = factories.create(models.Upload)

		video = factories.create(
			models.Video,
			title='Vid 1',
			slug='vid-1',
			poster=image,
			og_image=image
		)
		transcoding = factories.create(
			models.Transcoding,
			video=video,
			quality='480p',
			type='video/webm; codecs="vp8, vorbis"',
			upload=movie,
		)

		resp:HttpResponse = self.client.get(
			reverse('video', args=['vid-1']) + '?quality=720p')

		self.assertEqual(resp.status_code, 200)

		content:str = resp.content.decode(resp.charset)

		self.assertInHTML(
			"""<video width="853" height="480" poster="{image}" controls="controls">
				<source src="{url}" type='video/webm; codecs="vp8, vorbis"' />
				You need a browser that understands HTML5 video and supports vp8 codecs.
			</video>""".format(url=movie.file.url, image=image.file.url),
			content,
		)

		self.assertInHTML(
			'<meta property="og:image" content="{image}" />'.format(image=image.file.url),
			content,
		)


class VideoWithTrackTestCase(UploadMixin, TestCase):
	def setUp(self):
		super().setUp()
		self.client = Client()
		self.video = factories.create(
			models.Video,
			title='Vid 1',
			slug='vid-1',
			default_quality='480p',
		)
		factories.create(
			models.Transcoding,
			video=self.video,
			quality='480p',
			type='video/webm; codecs="vp9, opus"',
			url='http://480p.webm',
		)
		factories.create(
			models.Transcoding,
			video=self.video,
			quality='480p',
			type='video/mp4',
			url='http://480p.mp4',
		)

	def test_video_view_renders_track_properly(self):

		factories.create(
			models.Track,
			video=self.video,
			lang='en',
		)

		resp:HttpResponse = self.client.get(reverse('video', args=['vid-1']))

		self.assertEqual(resp.status_code, 200)

		content:str = resp.content.decode(resp.charset)

		self.assertInHTML(
			"""<video width="853" height="480" controls="controls">
				<source src="http://480p.webm" type='video/webm; codecs="vp9, opus"' />
				<source src="http://480p.mp4" type='video/mp4' />
				<track src="/uploads/some_file.txt" srclang="en" kind="subtitles" label="en" />
				You need a browser that understands HTML5 video and supports h.264 or vp9 codecs.
			</video>""",
			content,
		)

	def test_video_view_renders_multiple_tracks_properly(self):

		track_en = factories.create(
			models.Track,
			video=self.video,
			lang='en',
		)

		track_nl = factories.create(
			models.Track,
			video=self.video,
			lang='nl',
		)

		resp:HttpResponse = self.client.get(reverse('video', args=['vid-1']))

		self.assertEqual(resp.status_code, 200)

		content:str = resp.content.decode(resp.charset)

		self.assertInHTML(
			f"""<video width="853" height="480" controls="controls">
				<source src="http://480p.webm" type='video/webm; codecs="vp9, opus"' />
				<source src="http://480p.mp4" type='video/mp4' />
				<track src="{ track_en.upload.file.url }" srclang="en" kind="subtitles" label="en" />
				<track src="{ track_nl.upload.file.url }" srclang="nl" kind="subtitles" label="nl" />
				You need a browser that understands HTML5 video and supports h.264 or vp9 codecs.
			</video>""",
			content,
		)


	def test_video_view_renders_default_track_properly(self):

		factories.create(
			models.Track,
			video=self.video,
			lang='en',
			default=True
		)

		resp:HttpResponse = self.client.get(reverse('video', args=['vid-1']))

		self.assertEqual(resp.status_code, 200)

		content:str = resp.content.decode(resp.charset)

		self.assertInHTML(
			"""<video width="853" height="480" controls="controls">
				<source src="http://480p.webm" type='video/webm; codecs="vp9, opus"' />
				<source src="http://480p.mp4" type='video/mp4' />
				<track src="/uploads/some_file.txt" default="default" srclang="en" kind="subtitles" label="en" />
				You need a browser that understands HTML5 video and supports h.264 or vp9 codecs.
			</video>""",
			content,
		)

	def test_video_view_renders_multiple_tracks_properly_with_one_default(self):

		track_en = factories.create(
			models.Track,
			video=self.video,
			lang='en',
			default=True
		)

		track_nl = factories.create(
			models.Track,
			video=self.video,
			lang='nl',
		)

		resp:HttpResponse = self.client.get(reverse('video', args=['vid-1']))

		self.assertEqual(resp.status_code, 200)

		content:str = resp.content.decode(resp.charset)

		self.assertInHTML(
			f"""<video width="853" height="480" controls="controls">
				<source src="http://480p.webm" type='video/webm; codecs="vp9, opus"' />
				<source src="http://480p.mp4" type='video/mp4' />
				<track src="{ track_en.upload.file.url }" default="default" srclang="en" kind="subtitles" label="en" />
				<track src="{ track_nl.upload.file.url }" srclang="nl" kind="subtitles" label="nl" />
				You need a browser that understands HTML5 video and supports h.264 or vp9 codecs.
			</video>""",
			content,
		)

	def test_video_view_renders_track_label(self):

		factories.create(
			models.Track,
			video=self.video,
			lang='en',
			label='Some Label',
		)

		resp:HttpResponse = self.client.get(reverse('video', args=['vid-1']))

		self.assertEqual(resp.status_code, 200)

		content:str = resp.content.decode(resp.charset)

		self.assertInHTML(
			"""<video width="853" height="480" controls="controls">
				<source src="http://480p.webm" type='video/webm; codecs="vp9, opus"' />
				<source src="http://480p.mp4" type='video/mp4' />
				<track src="/uploads/some_file.txt" srclang="en" kind="subtitles" label="Some Label" />
				You need a browser that understands HTML5 video and supports h.264 or vp9 codecs.
			</video>""",
			content,
		)


	def test_video_view_renders_track_kind(self):

		factories.create(
			models.Track,
			video=self.video,
			lang='en',
			kind='captions',
		)

		resp:HttpResponse = self.client.get(reverse('video', args=['vid-1']))

		self.assertEqual(resp.status_code, 200)

		content:str = resp.content.decode(resp.charset)

		self.assertInHTML(
			"""<video width="853" height="480" controls="controls">
				<source src="http://480p.webm" type='video/webm; codecs="vp9, opus"' />
				<source src="http://480p.mp4" type='video/mp4' />
				<track src="/uploads/some_file.txt" srclang="en" kind="captions" label="en" />
				You need a browser that understands HTML5 video and supports h.264 or vp9 codecs.
			</video>""",
			content,
		)


class VideoWithCodecOrderCookieTestCase(UploadMixin, TestCase):
	""" Test the order of the codecs """
	def setUp(self):
		super().setUp()
		self.client = Client()

		self.video = factories.create(
			models.Video,
			title='Vid 1',
			slug='vid-1',
			default_quality='480p',
		)
		factories.create(
			models.Transcoding,
			video=self.video,
			quality='480p',
			type='video/mp4; codecs="avc1.64001e,mp4a.40.2"',
			url='http://480p.mp4',
		)
		factories.create(
			models.Transcoding,
			video=self.video,
			quality='480p',
			type='video/webm; codecs="vp9, opus"',
			url='http://480p.vp9.webm',
		)
		factories.create(
			models.Transcoding,
			video=self.video,
			quality='480p',
			type='video/webm; codecs="vp8, vorbis"',
			url='http://480p.vp8.webm',
		)

	def test_video_view_renders_transcoding_types_in_correct_order_without_cookie(self):

		resp:HttpResponse = self.client.get(reverse('video', args=['vid-1']))

		self.assertEqual(resp.status_code, 200)

		content:str = resp.content.decode(resp.charset)

		self.assertInHTML(
			"""<video width="853" height="480" controls="controls">
				<source src="http://480p.vp9.webm" type='video/webm; codecs="vp9, opus"' />
				<source src="http://480p.vp8.webm" type='video/webm; codecs="vp8, vorbis"' />
				<source src="http://480p.mp4" type='video/mp4; codecs="avc1.64001e,mp4a.40.2"' />
				You need a browser that understands HTML5 video and supports h.264 or vp8 or vp9 codecs.
			</video>""",
			content,
		)

	def test_video_view_renders_transcoding_types_in_correct_order_with_empty_cookie(self):

		self.client.cookies['video_codecs_prio'] = ''

		resp:HttpResponse = self.client.get(reverse('video', args=['vid-1']))

		self.assertEqual(resp.status_code, 200)

		content:str = resp.content.decode(resp.charset)

		self.assertInHTML(
			"""<video width="853" height="480" controls="controls">
				<source src="http://480p.vp9.webm" type='video/webm; codecs="vp9, opus"' />
				<source src="http://480p.vp8.webm" type='video/webm; codecs="vp8, vorbis"' />
				<source src="http://480p.mp4" type='video/mp4; codecs="avc1.64001e,mp4a.40.2"' />
				You need a browser that understands HTML5 video and supports h.264 or vp8 or vp9 codecs.
			</video>""",
			content,
		)

	def test_video_view_renders_transcoding_types_in_correct_order_with_only_vp8_mentioned(self):

		self.client.cookies['video_codecs_prio'] = 'vp8'
		resp:HttpResponse = self.client.get(reverse('video', args=['vid-1']))

		self.assertEqual(resp.status_code, 200)

		content:str = resp.content.decode(resp.charset)

		self.assertInHTML(
			"""<video width="853" height="480" controls="controls">
				<source src="http://480p.vp8.webm" type='video/webm; codecs="vp8, vorbis"' />
				<source src="http://480p.vp9.webm" type='video/webm; codecs="vp9, opus"' />
				<source src="http://480p.mp4" type='video/mp4; codecs="avc1.64001e,mp4a.40.2"' />
				You need a browser that understands HTML5 video and supports h.264 or vp8 or vp9 codecs.
			</video>""",
			content,
		)

	def test_video_view_renders_transcoding_types_in_correct_order_with_only_h264_mentioned(self):

		self.client.cookies['video_codecs_prio'] = 'h.264'
		resp:HttpResponse = self.client.get(reverse('video', args=['vid-1']))

		self.assertEqual(resp.status_code, 200)

		content:str = resp.content.decode(resp.charset)

		self.assertInHTML(
			"""<video width="853" height="480" controls="controls">
				<source src="http://480p.mp4" type='video/mp4; codecs="avc1.64001e,mp4a.40.2"' />
				<source src="http://480p.vp9.webm" type='video/webm; codecs="vp9, opus"' />
				<source src="http://480p.vp8.webm" type='video/webm; codecs="vp8, vorbis"' />
				You need a browser that understands HTML5 video and supports h.264 or vp8 or vp9 codecs.
			</video>""",
			content,
		)

	def test_video_view_renders_transcoding_types_in_correct_order_with_vp8_and_h264_mentioned(self):

		self.client.cookies['video_codecs_prio'] = 'vp8 h.264'
		resp:HttpResponse = self.client.get(reverse('video', args=['vid-1']))

		self.assertEqual(resp.status_code, 200)

		content:str = resp.content.decode(resp.charset)

		self.assertInHTML(
			"""<video width="853" height="480" controls="controls">
				<source src="http://480p.vp8.webm" type='video/webm; codecs="vp8, vorbis"' />
				<source src="http://480p.mp4" type='video/mp4; codecs="avc1.64001e,mp4a.40.2"' />
				<source src="http://480p.vp9.webm" type='video/webm; codecs="vp9, opus"' />
				You need a browser that understands HTML5 video and supports h.264 or vp8 or vp9 codecs.
			</video>""",
			content,
		)

	def test_video_view_renders_transcoding_types_in_correct_order_with_h264_and_vp8_mentioned(self):

		self.client.cookies['video_codecs_prio'] = 'h.264 vp8'
		resp:HttpResponse = self.client.get(reverse('video', args=['vid-1']))

		self.assertEqual(resp.status_code, 200)

		content:str = resp.content.decode(resp.charset)

		self.assertInHTML(
			"""<video width="853" height="480" controls="controls">
				<source src="http://480p.mp4" type='video/mp4; codecs="avc1.64001e,mp4a.40.2"' />
				<source src="http://480p.vp8.webm" type='video/webm; codecs="vp8, vorbis"' />
				<source src="http://480p.vp9.webm" type='video/webm; codecs="vp9, opus"' />
				You need a browser that understands HTML5 video and supports h.264 or vp8 or vp9 codecs.
			</video>""",
			content,
		)

	def test_video_view_renders_transcoding_types_in_correct_order_with_h264_and_vp9_and_vp8_mentioned(self):

		self.client.cookies['video_codecs_prio'] = 'h.264 vp9 vp8'
		resp:HttpResponse = self.client.get(reverse('video', args=['vid-1']))

		self.assertEqual(resp.status_code, 200)

		content:str = resp.content.decode(resp.charset)

		self.assertInHTML(
			"""<video width="853" height="480" controls="controls">
				<source src="http://480p.mp4" type='video/mp4; codecs="avc1.64001e,mp4a.40.2"' />
				<source src="http://480p.vp9.webm" type='video/webm; codecs="vp9, opus"' />
				<source src="http://480p.vp8.webm" type='video/webm; codecs="vp8, vorbis"' />
				You need a browser that understands HTML5 video and supports h.264 or vp8 or vp9 codecs.
			</video>""",
			content,
		)

	def test_video_view_renders_transcoding_types_in_correct_order_with_h264_and_vp8_and_vp9_mentioned(self):

		self.client.cookies['video_codecs_prio'] = 'h.264 vp8 vp9'
		resp:HttpResponse = self.client.get(reverse('video', args=['vid-1']))

		self.assertEqual(resp.status_code, 200)

		content:str = resp.content.decode(resp.charset)

		self.assertInHTML(
			"""<video width="853" height="480" controls="controls">
				<source src="http://480p.mp4" type='video/mp4; codecs="avc1.64001e,mp4a.40.2"' />
				<source src="http://480p.vp8.webm" type='video/webm; codecs="vp8, vorbis"' />
				<source src="http://480p.vp9.webm" type='video/webm; codecs="vp9, opus"' />
				You need a browser that understands HTML5 video and supports h.264 or vp8 or vp9 codecs.
			</video>""",
			content,
		)

	def test_video_view_renders_transcoding_types_ignores_garbage_in_cookie(self):

		self.client.cookies['video_codecs_prio'] = 'bwarpblergh crap bla'
		resp:HttpResponse = self.client.get(reverse('video', args=['vid-1']))

		self.assertEqual(resp.status_code, 200)

		content:str = resp.content.decode(resp.charset)

		self.assertInHTML(
			"""<video width="853" height="480" controls="controls">
				<source src="http://480p.vp9.webm" type='video/webm; codecs="vp9, opus"' />
				<source src="http://480p.vp8.webm" type='video/webm; codecs="vp8, vorbis"' />
				<source src="http://480p.mp4" type='video/mp4; codecs="avc1.64001e,mp4a.40.2"' />
				You need a browser that understands HTML5 video and supports h.264 or vp8 or vp9 codecs.
			</video>""",
			content,
		)

	def test_video_view_renders_transcoding_types_in_correct_order_with_h264_and_vp8_and_crap_and_vp9_mentioned(self):

		self.client.cookies['video_codecs_prio'] = 'h.264 vp8 nonexistent-thing vp9'
		resp:HttpResponse = self.client.get(reverse('video', args=['vid-1']))

		self.assertEqual(resp.status_code, 200)

		content:str = resp.content.decode(resp.charset)

		self.assertInHTML(
			"""<video width="853" height="480" controls="controls">
				<source src="http://480p.mp4" type='video/mp4; codecs="avc1.64001e,mp4a.40.2"' />
				<source src="http://480p.vp8.webm" type='video/webm; codecs="vp8, vorbis"' />
				<source src="http://480p.vp9.webm" type='video/webm; codecs="vp9, opus"' />
				You need a browser that understands HTML5 video and supports h.264 or vp8 or vp9 codecs.
			</video>""",
			content,
		)
