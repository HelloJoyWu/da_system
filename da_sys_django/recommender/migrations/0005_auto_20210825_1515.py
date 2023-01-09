# Generated by Django 3.2.5 on 2021-08-25 07:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recommender', '0004_auto_20210825_1441'),
    ]

    operations = [
        migrations.AlterField(
            model_name='setuplog',
            name='create_time',
            field=models.DateTimeField(auto_now_add=True, help_text='Setup create time always UTC+0'),
        ),
        migrations.AlterField(
            model_name='setuplog',
            name='end_time',
            field=models.DateTimeField(editable=False, help_text='End Time always UTC+0'),
        ),
        migrations.AlterField(
            model_name='setuplog',
            name='start_time',
            field=models.DateTimeField(editable=False, help_text='Start Time always UTC+0'),
        ),
    ]
