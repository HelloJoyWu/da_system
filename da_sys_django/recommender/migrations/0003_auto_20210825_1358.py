# Generated by Django 3.2.5 on 2021-08-25 05:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recommender', '0002_auto_20210819_1128'),
    ]

    operations = [
        migrations.RenameModel('RecommendSetupLog', 'SetupLog'),
        migrations.RenameField('SetupLog', 'start_time', 'start'),
        migrations.RenameField('SetupLog', 'end_time', 'end'),
        migrations.AlterField('SetupLog', 'start', models.CharField(help_text='Setup start Time', max_length=20)),
        migrations.AlterField('SetupLog', 'end', models.CharField(help_text='Setup end Time', max_length=20)),
        migrations.RenameField('SetupLog', 'currency', 'currency_name'),
        migrations.AlterField('SetupLog', 'currency_name', models.CharField(max_length=10, help_text='Setup currency')),
        migrations.AddField('SetupLog', 'currency', models.CharField(help_text='Currency', max_length=20)),
        migrations.AddField('SetupLog', 'start_time', models.DateTimeField(help_text='Start Time')),
        migrations.AddField('SetupLog', 'end_time', models.DateTimeField(help_text='End Time')),
    ]
