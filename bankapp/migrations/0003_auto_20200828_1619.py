# Generated by Django 2.2.14 on 2020-08-28 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bankapp', '0002_bankaccountdetails_account_balance'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bankaccountdetails',
            name='BVN',
        ),
        migrations.RemoveField(
            model_name='bankaccountdetails',
            name='account_reference',
        ),
        migrations.RemoveField(
            model_name='bankaccountdetails',
            name='reservation_reference',
        ),
        migrations.AddField(
            model_name='bankaccountdetails',
            name='bank_slug',
            field=models.SlugField(default='', max_length=30, verbose_name='Bank Slug'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='bankaccountdetails',
            name='customer_code',
            field=models.CharField(default='', max_length=40, verbose_name='Customer Code'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='bankaccountdetails',
            name='customer_id',
            field=models.CharField(default='', max_length=10, verbose_name='Customer ID'),
            preserve_default=False,
        ),
    ]