# Generated by Django 4.2.7 on 2023-11-07 09:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('access_log', '0003_unwantedhit_status_code'),
    ]

    operations = [
        migrations.CreateModel(
            name='Successful_url',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('IP_ADDRESS', models.GenericIPAddressField()),
                ('URL', models.URLField()),
            ],
        ),
    ]
