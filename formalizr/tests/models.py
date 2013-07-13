from django.db import models


class SimpleModel(models.Model):
    value = models.IntegerField(blank=False)

    class Meta:
        app_label = 'formalizr'