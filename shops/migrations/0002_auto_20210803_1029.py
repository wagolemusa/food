# Generated by Django 2.2.16 on 2021-08-03 10:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shops', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='billingaddress',
            name='apartment_address',
        ),
        migrations.RemoveField(
            model_name='billingaddress',
            name='street_address',
        ),
    ]