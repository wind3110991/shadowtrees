# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Myblog', '0002_remove_blog_mark'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='mark',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
