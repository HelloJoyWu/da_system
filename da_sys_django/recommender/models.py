from django.db import models

import logging

logger = logging.getLogger(__name__)


class Model(models.Model):
    objects = models.Manager()

    class Meta:
        abstract = True


class SetupLog(models.Model):
    start = models.CharField(help_text='Setup start Time', max_length=20)
    end = models.CharField(help_text='Setup end Time', max_length=20)
    timezone = models.CharField(help_text='Timezone with UTC format', max_length=10)
    timezone_diff = models.SmallIntegerField(help_text='Timezone difference value')  # Values from -32768 to 32767
    currency_name = models.CharField(help_text='Setup currency', max_length=10)
    currency = models.CharField(help_text='Currency', max_length=20)
    owner_names = models.TextField(help_text='Owner name')
    owner_ssids = models.TextField(help_text='Owner ssid')
    game_names = models.TextField(help_text='Game name')
    game_codes = models.TextField(help_text='Game code')
    start_time = models.DateTimeField(help_text='Start Time always UTC+0',  editable=False)
    end_time = models.DateTimeField(help_text='End Time always UTC+0',  editable=False)
    create_time = models.DateTimeField(help_text='Setup create time always UTC+0', auto_now_add=True)
    creator = models.CharField(help_text='Creator name depends on auth_user', max_length=150)
    game_names_en = models.CharField(help_text='Game name', max_length=200, default='')

    class Meta:
        ordering = ['-create_time']

    def __str__(self):
        """
        String for representing the MyModelName object (in Admin site etc.).
        """
        return 'log_' + str(self.create_time)
