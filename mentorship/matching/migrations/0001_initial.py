# Generated by Django 2.1.2 on 2018-10-20 05:00

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CommunicationPlatform',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('communication_platform', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language_name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('phone_number', models.CharField(max_length=50)),
                ('city', models.CharField(max_length=50)),
                ('province_state_region', models.CharField(max_length=50)),
                ('country', models.CharField(max_length=50)),
                ('timezone', models.CharField(max_length=50)),
                ('sponsor_stage', models.CharField(max_length=50)),
                ('faith', models.CharField(max_length=50)),
                ('sponsor_type', models.CharField(max_length=50)),
                ('refugee_region', models.CharField(max_length=50)),
                ('communication_platforms', models.ManyToManyField(to='matching.CommunicationPlatform')),
                ('languages', models.ManyToManyField(to='matching.Language')),
            ],
        ),
        migrations.CreateModel(
            name='SponsorComponent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sponsor_component', models.CharField(max_length=50)),
            ],
        ),
        migrations.AddField(
            model_name='profile',
            name='sponsor_components',
            field=models.ManyToManyField(to='matching.SponsorComponent'),
        ),
    ]
