# Generated by Django 4.0.4 on 2022-05-20 14:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('snapvisite', '0025_alter_companyday_options_alter_timeslot_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='payment_status',
            field=models.BooleanField(default=False),
        ),
    ]