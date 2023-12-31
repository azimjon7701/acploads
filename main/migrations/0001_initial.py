# Generated by Django 3.2.15 on 2022-08-05 16:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('owner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='companies', to='account.profile')),
            ],
        ),
        migrations.CreateModel(
            name='Search',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('published_date', models.DateField(blank=True, null=True)),
                ('origin', models.CharField(blank=True, max_length=255, null=True)),
                ('dh_o', models.FloatField(blank=True, null=True)),
                ('destination', models.CharField(blank=True, max_length=255, null=True)),
                ('dh_d', models.FloatField(blank=True, null=True)),
                ('distance', models.FloatField(blank=True, null=True)),
                ('length', models.FloatField(blank=True, null=True)),
                ('wieght', models.FloatField(blank=True, null=True)),
                ('owner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='searches', to='account.profile')),
            ],
        ),
        migrations.CreateModel(
            name='Load',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('published_date', models.DateField(auto_now_add=True)),
                ('origin', models.CharField(max_length=255)),
                ('dh_o', models.FloatField()),
                ('destination', models.CharField(max_length=255)),
                ('dh_d', models.FloatField()),
                ('distance', models.FloatField()),
                ('length', models.FloatField()),
                ('wieght', models.FloatField()),
                ('price', models.FloatField()),
                ('suggested_price', models.FloatField()),
                ('company', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='loads', to='main.company')),
            ],
        ),
    ]
