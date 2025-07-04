from django.db import models


class AlterFieldModel(models.Model):
    data = models.JSONField()
