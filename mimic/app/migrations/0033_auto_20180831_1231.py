# Generated by Django 2.0.6 on 2018-08-31 12:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0032_auto_20180831_1228'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alternativename',
            name='protein',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Protein'),
        ),
    ]
