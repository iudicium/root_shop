# Generated by Django 4.2.3 on 2023-08-04 09:10

import app_orders.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('app_catalog', '0001_initial'),
        ('app_users', '__first__'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('createdAt', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('fullName', models.CharField(max_length=255, verbose_name='Full Name')),
                ('email', models.EmailField(max_length=254, verbose_name='Email')),
                ('phone', models.CharField(max_length=20, verbose_name='Phone')),
                ('deliveryType', models.CharField(choices=[('normal', 'Normal Delivery'), ('express', 'Express Delivery')], default='normal', max_length=50, verbose_name='Delivery Type')),
                ('delivery_price', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Delivery Cost')),
                ('paymentType', models.CharField(choices=[('card', 'Payment with Card'), ('different_card', "Payment with Somebody Else's Card")], default='card', max_length=50, verbose_name='Payment Type')),
                ('totalCost', models.DecimalField(decimal_places=2, max_digits=8, verbose_name='Total Cost')),
                ('status', models.CharField(blank=True, max_length=50, null=True, verbose_name='Status')),
                ('city', models.CharField(max_length=100, verbose_name='City')),
                ('address', models.CharField(max_length=255, verbose_name='Address')),
                ('user_profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_users.profile', verbose_name='User')),
            ],
            options={
                'verbose_name': 'Order',
                'verbose_name_plural': 'Orders',
                'ordering': ('-createdAt',),
            },
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=16, verbose_name='Payment Number')),
                ('name', models.CharField(max_length=255, verbose_name='Cardholder Name')),
                ('month', models.CharField(max_length=2, verbose_name='Expiration Month')),
                ('year', models.CharField(max_length=4, verbose_name='Expiration Year')),
                ('code', models.CharField(max_length=8, verbose_name='Security Code')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_orders.order')),
                ('user', models.ForeignKey(default=app_orders.models.get_user_default, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name': 'Payment',
                'verbose_name_plural': 'Payments',
            },
        ),
        migrations.CreateModel(
            name='OrderProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=8, verbose_name='Price')),
                ('quantity', models.PositiveIntegerField(default=1, verbose_name='Quantity')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_products', to='app_orders.order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_catalog.product')),
            ],
            options={
                'verbose_name': 'Order Product',
                'verbose_name_plural': 'Order Products',
            },
        ),
    ]
