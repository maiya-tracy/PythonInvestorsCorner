# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2019-06-27 21:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login_and_registration_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='has_usable_password',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
    ]
