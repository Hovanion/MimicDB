# Generated by Django 2.0.6 on 2022-07-17 18:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0058_auto_20220717_1750'),
    ]

    operations = [
        migrations.AlterField(
            model_name='protein',
            name='uniprot',
            field=models.CharField(max_length=24, unique=True),
        ),
    ]
