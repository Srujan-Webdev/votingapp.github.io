# Generated by Django 4.0.3 on 2022-03-19 11:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='is_admin_verified',
            field=models.BooleanField(default=False),
        ),
    ]
