# Generated by Django 2.0.6 on 2019-04-25 08:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0050_auto_20180912_0946'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proteininteractor',
            name='pdb',
            field=models.CharField(blank=True, max_length=4096, null=True),
        ),
    ]
