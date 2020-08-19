# Generated by Django 2.2.14 on 2020-08-19 04:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BankAccountDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, verbose_name='Full Name')),
                ('bank_name', models.CharField(max_length=30, verbose_name='Bank Name')),
                ('bank_code', models.CharField(max_length=3, verbose_name='Bank Code')),
                ('account_number', models.CharField(max_length=10, verbose_name='Account Number')),
                ('BVN', models.CharField(blank=True, max_length=11, verbose_name='Bank Verification Number')),
                ('currency_code', models.CharField(choices=[('NGN', 'Naira')], default='NGN', max_length=3, verbose_name='Currency Code')),
                ('reservation_reference', models.CharField(max_length=40, verbose_name='Reservation Reference')),
                ('account_reference', models.CharField(max_length=20, verbose_name='Account Reference')),
                ('status', models.CharField(choices=[('ACTIVE', 'Active'), ('INACTIVE', 'Inactive')], max_length=15, verbose_name='Account Status')),
                ('created_on', models.DateTimeField(verbose_name='Account Created on')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='account_details')),
            ],
            options={
                'verbose_name': 'Bank Account Detail',
                'verbose_name_plural': 'Bank Account Details',
            },
        ),
    ]
