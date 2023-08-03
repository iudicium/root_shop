# Generated by Django 4.2.3 on 2023-08-01 14:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("app_orders", "0002_alter_order_options_order_delivery_price_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="orderproduct",
            name="order",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="order_products",
                to="app_orders.order",
            ),
        ),
    ]
