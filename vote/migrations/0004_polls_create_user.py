# Generated by Django 4.0.3 on 2022-03-19 06:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('vote', '0003_polls_create_voted'),
    ]

    operations = [
        migrations.AddField(
            model_name='polls_create',
            name='user',
            field=models.ForeignKey(default=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
