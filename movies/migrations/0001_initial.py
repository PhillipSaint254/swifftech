# Generated by Django 4.0.5 on 2022-06-27 11:26

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('genre', models.CharField(max_length=2000)),
                ('description', models.TextField(default='Text Here', null=True)),
                ('logo', models.CharField(default='logo', max_length=2000)),
                ('date_of_release', models.DateField(null=True)),
                ('year', models.IntegerField()),
                ('rating', models.FloatField()),
                ('searches', models.IntegerField(default=0)),
                ('views', models.IntegerField(default=0)),
                ('seasons', models.IntegerField(default=0)),
                ('trailer', models.CharField(default='url', max_length=500)),
                ('movie', models.BooleanField(default=False)),
                ('video', models.CharField(default=None, max_length=500, null=True)),
                ('trending', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='TC',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=25)),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(default='', max_length=20)),
                ('amount', models.IntegerField(default=0)),
                ('transaction_code', models.CharField(max_length=20, unique=True)),
                ('code_stamp', models.CharField(default='some code', max_length=25)),
                ('created_at', models.DateTimeField(default=datetime.datetime(2022, 6, 27, 14, 26, 57, 751055, tzinfo=utc))),
                ('status', models.BooleanField(default=False)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Season',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unique_field', models.CharField(max_length=100, unique=True)),
                ('series_name', models.CharField(default=' ', max_length=50)),
                ('season_no', models.IntegerField(default=0)),
                ('series', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='all_seasons', to='movies.movie')),
            ],
        ),
        migrations.CreateModel(
            name='Sale',
            fields=[
                ('username', models.CharField(max_length=50)),
                ('transaction_type', models.CharField(choices=[('credit', 'credit'), ('debit', 'debit')], default='choose type', max_length=15)),
                ('item_sold', models.CharField(default='item', max_length=100)),
                ('price', models.IntegerField(default=0)),
                ('transaction_code', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('transaction_time', models.DateTimeField(default=datetime.datetime(2022, 6, 27, 14, 26, 57, 752054, tzinfo=utc))),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('requested_at', models.DateTimeField(default=datetime.datetime(2022, 6, 27, 14, 26, 57, 749039, tzinfo=utc))),
                ('downloaded', models.BooleanField(default=False)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Messages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.CharField(default='', max_length=2000)),
                ('created_at', models.DateTimeField(default=datetime.datetime(2022, 6, 27, 14, 26, 57, 752054, tzinfo=utc))),
                ('to', models.CharField(default='all', max_length=50)),
                ('unread', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Episode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('series_name', models.CharField(default=' ', max_length=50)),
                ('unique_field', models.CharField(max_length=100, unique=True)),
                ('season_no', models.IntegerField(default=0)),
                ('video', models.CharField(default=None, max_length=500, null=True)),
                ('no_of_episodes', models.IntegerField(default=0)),
                ('season', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='all_episodes', to='movies.season')),
            ],
        ),
        migrations.CreateModel(
            name='Details',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(default='username', max_length=20)),
                ('subscription', models.CharField(choices=[('not subscribed', 'not subscribed'), ('standard', 'standard'), ('pro', 'pro'), ('pro max', 'pro max')], default='not subscribed', max_length=20)),
                ('subscription_date', models.DateTimeField(default=datetime.datetime(2022, 6, 27, 14, 26, 57, 749039, tzinfo=utc))),
                ('phone', models.CharField(default='number', max_length=15)),
                ('coins', models.IntegerField(default=0)),
                ('points', models.FloatField(default=0)),
                ('epic', models.IntegerField(default=0)),
                ('drama', models.IntegerField(default=0)),
                ('horror', models.IntegerField(default=0)),
                ('comedy', models.IntegerField(default=0)),
                ('fantasy', models.IntegerField(default=0)),
                ('sci_fy', models.IntegerField(default=0)),
                ('fiction', models.IntegerField(default=0)),
                ('historical_film', models.IntegerField(default=0)),
                ('investigative', models.IntegerField(default=0)),
                ('thriller', models.IntegerField(default=0)),
                ('romance', models.IntegerField(default=0)),
                ('mystery', models.IntegerField(default=0)),
                ('action', models.IntegerField(default=0)),
                ('sitcom', models.IntegerField(default=0)),
                ('adventure', models.IntegerField(default=0)),
                ('war', models.IntegerField(default=0)),
                ('musical', models.IntegerField(default=0)),
                ('documentary', models.IntegerField(default=0)),
                ('western', models.IntegerField(default=0)),
                ('crime', models.IntegerField(default=0)),
                ('sports', models.IntegerField(default=0)),
                ('disaster', models.IntegerField(default=0)),
                ('biographical', models.IntegerField(default=0)),
                ('animation', models.IntegerField(default=0)),
                ('christian', models.IntegerField(default=0)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.CharField(max_length=500)),
                ('useful', models.BooleanField(default=False)),
                ('username', models.CharField(max_length=20)),
                ('date', models.DateTimeField(default=datetime.datetime(2022, 6, 27, 14, 26, 57, 751055, tzinfo=utc))),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
