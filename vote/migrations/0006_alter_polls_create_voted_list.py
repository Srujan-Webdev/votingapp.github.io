# Generated by Django 4.0.3 on 2022-03-21 11:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vote', '0005_polls_create_voted_list'),
    ]

    operations = [
        migrations.AlterField(
            model_name='polls_create',
            name='voted_list',
            field=models.IntegerField(),
        ),
    ]
