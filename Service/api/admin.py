from django.contrib import admin

from api.models import Audio

@admin.register(Audio)
class AudioAdmin(admin.ModelAdmin):
    list_display = ['id', 'raw_file', 'denoised', 'transformed', 'timestamp']
