# Generated by Django 3.2.15 on 2022-09-23 20:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0018_rename_value_distance_distance'),
    ]

    operations = [
        migrations.AlterField(
            model_name='load',
            name='destination',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
