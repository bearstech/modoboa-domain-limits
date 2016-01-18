# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin', '0003_auto_20151118_1215'),
    ]

    operations = [
        migrations.CreateModel(
            name='DomainLimit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('mail_limit', models.IntegerField(default=-1)),
                ('alias_limit', models.IntegerField(default=-1)),
                ('domain', models.OneToOneField(to='admin.Domain')),
            ],
            options={
                'db_table': 'domain_limits',
            },
        ),
    ]
