# analyzer/models.py
from django.db import models

class UnwantedHit(models.Model):
    ip_address = models.GenericIPAddressField()
    url = models.URLField()

    status_code=models.IntegerField(null=True)
    count = models.IntegerField(null=True)
    # timestamp = models.DateTimeField(auto_now_add=True)

class Successful_url(models.Model):
    IP_ADDRESS = models.GenericIPAddressField()
    URL = models.URLField()

