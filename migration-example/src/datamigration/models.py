from django.db import models

from jsonfield import fields


class DataMigrationModel(models.Model):
    data = models.JSONField()
