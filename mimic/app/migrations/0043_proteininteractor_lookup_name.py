# Generated by Django 2.0.6 on 2018-09-08 06:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0042_proteininteractor_function'),
    ]

    operations = [
        migrations.AddField(
            model_name='proteininteractor',
            name='lookup_name',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
    ]
