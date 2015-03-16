# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Myblog', '0003_blog_mark'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blog',
            name='mark',
        ),
    ]
