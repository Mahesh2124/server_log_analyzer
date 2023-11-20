# analyzer/models.py
from django.db import models

class Redirection(models.Model):
    ip_address = models.GenericIPAddressField()
    url = models.URLField()
    timestamp = models.CharField(max_length=255,default='hello')
    status_code=models.IntegerField(null=True)
    count = models.IntegerField(null=True)

class Client_errors(models.Model):
    ip_address = models.GenericIPAddressField()
    url = models.URLField()
    timestamp = models.CharField(max_length=255,default='hello')
    status_code=models.IntegerField(null=True)
    count = models.IntegerField(null=True)

class Server_errors(models.Model):
    ip_address = models.GenericIPAddressField()
    url = models.URLField()
    timestamp = models.CharField(max_length=255,default='hello')
    status_code=models.IntegerField(null=True)
    count = models.IntegerField(null=True)

class Successful_url(models.Model):
    IP_ADDRESS = models.GenericIPAddressField()
    URL = models.URLField()

