
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "log_project.settings")
import django
django.setup()






from access_log.models import UnwantedHit  # Replace 'your_app' with the actual name of your Django app
from access_log.models import Successful_url
# Delete all data from the UnwantedHit model
# UnwantedHit.objects.all().delete()
x = UnwantedHit.objects.all().values()
y= Successful_url.objects.all().values()
print(x)
print(y)
UnwantedHit.objects.all().delete()
Successful_url.objects.all().delete()
