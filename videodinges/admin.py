from typing import Iterable

from django import forms
from django.contrib import admin
from django.core.exceptions import ValidationError

from . import models

class TranscodingsForm(forms.ModelForm):
	def clean(self):
		cleaned_data = super().clean()
		if not cleaned_data['url'] and not cleaned_data['upload']:
			validation_error = ValidationError('Either url or upload must be given', code='invalid')
			self.add_error('url', validation_error)
			self.add_error('upload', validation_error)
		if cleaned_data['url'] and cleaned_data['upload']:
			validation_error = ValidationError('Cannot fill both url and upload', code='invalid')
			self.add_error('url', validation_error)
			self.add_error('upload', validation_error)
		return cleaned_data

class TrackInlineFormset(forms.BaseInlineFormSet):
	forms: Iterable[forms.ModelForm]
	def clean(self):
		cleaned_data = super().clean()
		default_cnt = 0
		for form in self.forms:
			try:
				if form.cleaned_data['default'] is True:
					default_cnt += 1
			except AttributeError:
				pass
			if default_cnt > 1:
				form.add_error('default', ValidationError('Can set only one track as default'))
		return cleaned_data

class TranscodingsInline(admin.StackedInline):
	model = models.Transcoding
	form = TranscodingsForm
	fields = ['quality', 'type', 'url', 'upload']
	extra = 0

class TracksInline(admin.StackedInline):
	model = models.Track
	formset = TrackInlineFormset
	fields = ('default', 'kind', 'lang', 'label', 'upload')
	extra = 0

class VideoAdmin(admin.ModelAdmin):
	model = models.Video
	fields = ['title', 'description', 'slug', 'poster', 'og_image', 'created_at', 'default_quality']
	inlines = (TranscodingsInline, TracksInline)
	list_display = ('title', 'slug', 'created_at', 'updated_at')
	ordering = ('-created_at', )

admin.site.register(models.Video, VideoAdmin)
admin.site.register(models.Upload)
