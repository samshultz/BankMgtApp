# Generated by Django 2.2.14 on 2020-08-28 22:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('OTP_Auth', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='phonenumber',
            field=models.CharField(default='', max_length=14, verbose_name='Phone Number'),
            preserve_default=False,
        ),
    ]
