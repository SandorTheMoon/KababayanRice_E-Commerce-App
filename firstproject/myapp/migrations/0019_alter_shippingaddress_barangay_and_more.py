# Generated by Django 5.0.4 on 2024-05-18 16:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0018_product_product_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shippingaddress',
            name='barangay',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='shippingaddress',
            name='city',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='shippingaddress',
            name='home_address',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='shippingaddress',
            name='postal_code',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='shippingaddress',
            name='province',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='shippingaddress',
            name='region',
            field=models.CharField(default='', max_length=255),
        ),
    ]