# Generated by Django 5.1.3 on 2024-11-20 05:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0006_order_productorders_ordersusers'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]