# Generated by Django 2.0.6 on 2018-07-10 11:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_auto_20180710_1151'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dimer',
            name='name',
            field=models.CharField(editable=False, max_length=30, unique=True),
        ),
    ]
