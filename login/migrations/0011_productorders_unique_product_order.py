# Generated by Django 5.1.3 on 2024-11-24 11:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0010_alter_productorders_product_ordered'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='productorders',
            constraint=models.UniqueConstraint(fields=('order_id', 'product_id'), name='unique_product_order'),
        ),
    ]
