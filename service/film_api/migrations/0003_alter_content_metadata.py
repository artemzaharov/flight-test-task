# Generated by Django 4.1.7 on 2023-03-05 20:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('film_api', '0002_channel_parents_count'),
    ]

    operations = [
        migrations.AlterField(
            model_name='content',
            name='metadata',
            field=models.JSONField(blank=True, default=None, null=True),
        ),
    ]