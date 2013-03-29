from django.db import models


class OpenCivicID(models.Model):
    id = models.CharField(max_length=128, primary_key=True)
    internal_id = models.CharField(max_length=128)
    start = models.DateTimeField()
    end = models.DateTimeField(null=True)

    def __unicode__(self):
        return self.id
