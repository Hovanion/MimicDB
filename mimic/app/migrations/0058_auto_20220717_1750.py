# Generated by Django 2.0.6 on 2022-07-17 17:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0057_auto_20220717_1744'),
    ]

    operations = [
        migrations.RenameField(
            model_name='proteininformation',
            old_name='organism',
            new_name='organism_common',
        ),
    ]
