# Generated by Django 5.0.4 on 2024-05-13 14:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0012_rename_product_original_location_product_product_origin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='product_price',
            field=models.DecimalField(decimal_places=2, max_digits=4),
        ),
    ]
