# Generated by Django 4.2 on 2024-01-01 13:08

import analyse.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analyse', '0007_alter_data_release_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='data',
            name='release_date',
            field=models.DateField(default=analyse.models.random_date_2022_2023),
        ),
    ]
