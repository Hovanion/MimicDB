# Generated by Django 2.0.6 on 2018-09-10 13:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0045_auto_20180908_0707'),
    ]

    operations = [
        migrations.AddField(
            model_name='proteininteractor',
            name='annotated',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
    ]
