# Generated by Django 2.0.6 on 2018-07-23 13:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0017_auto_20180723_1340'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pdb',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pdb', models.CharField(max_length=4, unique=True)),
                ('exp_tech', models.CharField(choices=[('NMR', 'NMR'), ('X-ray', 'X-ray'), ('Electron Microscopy', 'Electron Microscopy'), ('Model', 'Model')], max_length=20)),
                ('resolution', models.FloatField(blank=True, null=True)),
                ('other_interactors', models.CharField(blank=True, max_length=200, null=True)),
                ('alpha', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pdb_alpha', to='app.Monomer')),
                ('alpha_domain', models.ManyToManyField(related_name='pdb_alpha_domain', to='app.Structure')),
                ('beta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pdb_beta', to='app.Monomer')),
                ('beta_domain', models.ManyToManyField(related_name='pdb_beta_domain', to='app.Structure')),
            ],
        ),
        migrations.CreateModel(
            name='PdbToProtein',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start', models.IntegerField()),
                ('stop', models.IntegerField()),
                ('pdb', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Pdb')),
            ],
        ),
        migrations.CreateModel(
            name='Protein',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uniprot', models.CharField(max_length=6, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='pdbtoprotein',
            name='protein',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Protein'),
        ),
        migrations.AddField(
            model_name='pdb',
            name='protein',
            field=models.ManyToManyField(blank=True, null=True, through='app.PdbToProtein', to='app.Protein'),
        ),
        migrations.AlterUniqueTogether(
            name='pdbtoprotein',
            unique_together={('pdb', 'protein')},
        ),
    ]
