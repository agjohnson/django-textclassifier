# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TrainingData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('app_label', models.CharField(max_length=100, verbose_name='Application name')),
                ('model', models.CharField(max_length=100, verbose_name='Model class name')),
                ('field_name', models.CharField(max_length=100, verbose_name='Field name')),
                ('data', models.TextField(blank=True, null=True, verbose_name='Training data')),
                ('create_date', models.DateTimeField(auto_now_add=True, verbose_name='Creation date')),
                ('update_date', models.DateTimeField(auto_now=True, verbose_name='Last modification date')),
            ],
            options={
                'verbose_name_plural': 'training data',
            },
        ),
        migrations.AlterUniqueTogether(
            name='trainingdata',
            unique_together=set([('app_label', 'model', 'field_name')]),
        ),
    ]
