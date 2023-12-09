# Generated by Django 3.2.15 on 2022-12-14 21:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0013_alter_comment_content'),
        ('main', '0022_auto_20221129_0223'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='owner',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='company', to='account.profile'),
        ),
    ]
