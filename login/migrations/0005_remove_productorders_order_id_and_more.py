# Generated by Django 5.1.3 on 2024-11-20 04:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0004_remove_order_product_id_productorders_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productorders',
            name='order_id',
        ),
        migrations.RemoveField(
            model_name='ordersusers',
            name='order_id',
        ),
        migrations.RemoveField(
            model_name='ordersusers',
            name='username',
        ),
        migrations.RemoveField(
            model_name='productorders',
            name='product_id',
        ),
        migrations.DeleteModel(
            name='Order',
        ),
        migrations.DeleteModel(
            name='OrdersUsers',
        ),
        migrations.DeleteModel(
            name='ProductOrders',
        ),
    ]