# Generated by Django 4.0.3 on 2022-03-21 13:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vote', '0011_alter_polls_create_voted_info'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='polls_create',
            name='voted_info',
        ),
    ]
