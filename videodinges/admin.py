from django.contrib import admin

from . import models

class TranscodingsInline(admin.TabularInline):
	model = models.Transcoding
	fields = ['quality', 'file']
	extra = 0

class VideoAdmin(admin.ModelAdmin):
	model = models.Video
	fields = ['title', 'description', 'slug']
	inlines = [TranscodingsInline]

admin.site.register(models.Video, VideoAdmin)