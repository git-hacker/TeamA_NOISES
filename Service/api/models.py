from django.db import models


class Audio(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    raw_file = models.FileField(null=False, blank=False)
    remark = models.CharField(blank=True, max_length=15)
    denoised = models.FileField(blank=True, null=True)
    transformed = models.FileField(blank=True, null=True)