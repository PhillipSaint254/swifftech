# Generated by Django 4.0.5 on 2022-07-05 05:36

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 7, 5, 8, 36, 38, 528279, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='details',
            name='coins',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='details',
            name='subscription_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 7, 5, 8, 36, 38, 524282, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='messages',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 7, 5, 8, 36, 38, 529280, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='request',
            name='requested_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 7, 5, 8, 36, 38, 523282, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='sale',
            name='transaction_time',
            field=models.DateTimeField(default=datetime.datetime(2022, 7, 5, 8, 36, 38, 529280, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 7, 5, 8, 36, 38, 527281, tzinfo=utc)),
        ),
    ]
