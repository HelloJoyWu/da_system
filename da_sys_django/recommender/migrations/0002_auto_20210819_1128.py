# Generated by Django 3.2.5 on 2021-08-19 03:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recommender', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recommendsetuplog',
            name='owner_names',
            field=models.TextField(help_text='Owner name'),
        ),
        migrations.AlterField(
            model_name='recommendsetuplog',
            name='owner_ssids',
            field=models.TextField(help_text='Owner ssid'),
        ),
    ]
