# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Myblog', '0004_remove_blog_mark'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='markCount',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
