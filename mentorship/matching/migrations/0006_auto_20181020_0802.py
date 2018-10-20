# Generated by Django 2.1.2 on 2018-10-20 12:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('matching', '0005_auto_20181020_0642'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mentorship',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='mentorship',
            name='is_pending',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='mentorship',
            name='mentee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mentors', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='mentorship',
            name='mentor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mentees', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='profile',
            name='years_of_exp',
            field=models.IntegerField(default=0),
        ),
    ]