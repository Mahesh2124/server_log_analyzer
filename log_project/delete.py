
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "log_project.settings")
import django
django.setup()






from access_log.models import Redirection  # Replace 'your_app' with the actual name of your Django app
from access_log.models import Successful_url,Server_errors,Client_errors
# Delete all data from the UnwantedHit model
# UnwantedHit.objects.all().delete()
x = Redirection.objects.all().values()
y= Successful_url.objects.all().values()
z=Server_errors.objects.all().values()
l=Client_errors.objects.all().values()
print(x)
print(y)
print(z)
print(l)
# Redirection.objects.all().delete()
# Server_errors.objects.all().delete()
# Client_errors.objects.all().delete()
# Successful_url.objects.all().delete()
