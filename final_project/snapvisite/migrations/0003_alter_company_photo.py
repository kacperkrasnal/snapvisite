# Generated by Django 4.0.4 on 2022-04-30 16:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('snapvisite', '0002_remove_company_category_company_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='company_photo/'),
        ),
    ]