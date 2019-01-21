# Generated by Django 2.0.5 on 2018-06-06 13:52

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0007_auto_20180602_1129'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='price',
        ),
        migrations.RemoveField(
            model_name='product',
            name='url',
        ),
        migrations.AddField(
            model_name='product',
            name='best_price',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
        migrations.AddField(
            model_name='product',
            name='best_url',
            field=models.URLField(default='no-url'),
        ),
        migrations.AddField(
            model_name='product',
            name='best_vendor',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AddField(
            model_name='product',
            name='listings',
            field=django.contrib.postgres.fields.jsonb.JSONField(default=[]),
        ),
    ]