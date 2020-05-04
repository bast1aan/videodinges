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

class TranscodingsInline(admin.StackedInline):
	model = models.Transcoding
	form = TranscodingsForm
	fields = ['quality', 'url', 'upload']
	#inline = [UploadsInline]
	extra = 0

class VideoAdmin(admin.ModelAdmin):
	model = models.Video
	fields = ['title', 'description', 'slug']
	inlines = [TranscodingsInline]

admin.site.register(models.Video, VideoAdmin)
admin.site.register(models.Upload)
