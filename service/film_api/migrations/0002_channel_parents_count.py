# Generated by Django 4.1.7 on 2023-03-05 17:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('film_api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='channel',
            name='parents_count',
            field=models.IntegerField(default=0),
        ),
    ]