# Generated by Django 4.2 on 2024-01-01 12:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analyse', '0003_remove_data_champ_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='data',
            name='release_date',
            field=models.DateField(default=-1),
            preserve_default=False,
        ),
    ]
