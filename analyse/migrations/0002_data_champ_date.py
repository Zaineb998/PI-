# Generated by Django 4.2 on 2023-12-31 16:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analyse', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='data',
            name='champ_date',
            field=models.DateField(default=1),
            preserve_default=False,
        ),
    ]
