# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-08-14 09:37
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Posts', '0008_auto_20170810_0201'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post_views',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.CharField(max_length=40)),
                ('session', models.CharField(max_length=40, null=True)),
                ('created', models.DateTimeField(default=datetime.datetime(2017, 8, 14, 15, 7, 49, 354821))),
                ('entry', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post_views', to='Posts.PostModel')),
            ],
            options={
                'verbose_name_plural': 'Post_views',
            },
        ),
    ]