# Generated by Django 2.0.6 on 2018-09-05 05:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0037_auto_20180904_1237'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dimertoproteininteractor',
            name='pmid',
        ),
        migrations.AddField(
            model_name='dimertoproteininteractor',
            name='reference',
            field=models.CharField(default='TMP_REF', max_length=512),
            preserve_default=False,
        ),
    ]
