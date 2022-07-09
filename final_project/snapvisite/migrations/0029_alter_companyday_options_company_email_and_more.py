# Generated by Django 4.0.4 on 2022-05-21 14:25

from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('snapvisite', '0028_appointment_appointment_code'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='companyday',
            options={'ordering': ('date',), 'verbose_name': 'company day', 'verbose_name_plural': 'company days'},
        ),
        migrations.AddField(
            model_name='company',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='company',
            name='phone_number',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region=None),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='appointment_code',
            field=models.CharField(default='123', max_length=50),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='payment_status',
            field=models.BooleanField(choices=[(True, 'Pay with card now'), (False, 'Pay by cash on visit')], default=False),
        ),
        migrations.AlterField(
            model_name='service',
            name='time',
            field=models.IntegerField(default=30, help_text="    Put time in minutes. Like '60' = 1h, '30' = 30min, '90' = 1h 30min"),
        ),
    ]