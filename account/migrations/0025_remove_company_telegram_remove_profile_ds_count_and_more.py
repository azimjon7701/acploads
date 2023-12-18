# Generated by Django 5.0 on 2023-12-17 14:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0024_authtoken'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='company',
            name='telegram',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='ds_count',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='ff_count',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='loc',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='lofc',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='los',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='nc_count',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='np_count',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='ri',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='sop',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='ui_count',
        ),
        migrations.AddField(
            model_name='comment',
            name='dislikes',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='comment',
            name='likes',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='company',
            name='address1',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='company',
            name='address2',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='company',
            name='authority',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='company',
            name='city',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='company',
            name='country',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='company',
            name='credit_score',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='company',
            name='dba_name',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='company',
            name='entity_type',
            field=models.CharField(choices=[('Carrier', 'carrier'), ('Broker', 'broker')], default='Carrier', max_length=10),
        ),
        migrations.AddField(
            model_name='company',
            name='insurance',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='company',
            name='ms',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='company',
            name='other1',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='company',
            name='other2',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='company',
            name='state',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='company',
            name='usdot',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='company',
            name='w9',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='company',
            name='zip_code',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.CreateModel(
            name='CommentReaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.BooleanField(blank=True, null=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment_reactions', to='account.profile')),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_reactions', to='account.comment')),
            ],
        ),
        migrations.CreateModel(
            name='ReportComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sc', models.BooleanField(default=False, help_text='Sexual comment', verbose_name='Sexual comment')),
                ('vorc', models.BooleanField(default=False, help_text='Violent or repulsive comment', verbose_name='Violent or repulsive comment')),
                ('hoac', models.BooleanField(default=False, help_text='Hateful or abusive content', verbose_name='Hateful or abusive content')),
                ('hob', models.BooleanField(default=False, help_text='Harassment or bullying', verbose_name='Harassment or bullying')),
                ('hoda', models.BooleanField(default=False, help_text='Harmful or dangerous acts', verbose_name='Harmful or dangerous acts')),
                ('mis', models.BooleanField(default=False, help_text='Misinformation', verbose_name='Misinformation')),
                ('pt', models.BooleanField(default=False, help_text='Promotes terrorism', verbose_name='Promotes terrorism')),
                ('som', models.BooleanField(default=False, help_text='Spam or misleading', verbose_name='Spam or misleading')),
                ('li', models.BooleanField(default=False, help_text='Legal issue', verbose_name='Legal issue')),
                ('author_company', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='reports', to='account.company')),
                ('author_profile', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='reports', to='account.profile')),
                ('comment', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reports', to='account.comment')),
            ],
        ),
    ]