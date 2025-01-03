# Generated by Django 5.0.4 on 2024-05-22 08:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0025_alter_product_product_description_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='account',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='myapp.account'),
        ),
        migrations.AlterField(
            model_name='shippingaddress',
            name='account',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='myapp.account'),
        ),
    ]
