# Generated by Django 3.2.5 on 2021-08-25 06:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recommender', '0003_auto_20210825_1358'),
    ]

    operations = [
        migrations.AlterField(
            model_name='setuplog',
            name='end_time',
            field=models.DateTimeField(editable=False, help_text='End Time'),
        ),
        migrations.AlterField(
            model_name='setuplog',
            name='start_time',
            field=models.DateTimeField(editable=False, help_text='Start Time'),
        ),
    ]
