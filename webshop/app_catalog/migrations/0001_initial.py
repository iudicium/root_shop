# Generated by Django 4.2.3 on 2023-08-04 09:09

import app_catalog.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import taggit.managers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('taggit', '0005_auto_20220424_2025'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Title')),
                ('src', models.ImageField(upload_to='category_images/', verbose_name='Image Source')),
                ('alt', models.CharField(max_length=255, verbose_name='Alternative Text')),
                ('IsActive', models.BooleanField(default=False, verbose_name='Is Category Active?')),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, max_digits=8, verbose_name='Price')),
                ('count', models.IntegerField(verbose_name='Count')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='Date')),
                ('title', models.CharField(max_length=255, verbose_name='Title')),
                ('description', models.CharField(max_length=255, verbose_name='Description')),
                ('fullDescription', models.TextField(verbose_name='Full Description')),
                ('freeDelivery', models.BooleanField(verbose_name='Free Delivery')),
                ('rating', models.DecimalField(decimal_places=1, max_digits=3, verbose_name='Rating')),
                ('limited', models.BooleanField(default=False, verbose_name='Limtied Item?')),
                ('banner', models.BooleanField(default=False, verbose_name='Show on Banner?')),
                ('sale', models.BooleanField(default=False, verbose_name='Is item on sale?')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_catalog.category', verbose_name='Category')),
                ('tags', taggit.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags')),
            ],
            options={
                'verbose_name': 'Product',
                'verbose_name_plural': 'Products',
            },
        ),
        migrations.CreateModel(
            name='Subcategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Title')),
                ('src', models.ImageField(upload_to='subcategory_images/', verbose_name='Image Source')),
                ('alt', models.CharField(max_length=255, verbose_name='Alternative Text')),
                ('IsActive', models.BooleanField(default=False, verbose_name='Is SubCategory Active?')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subcategories', to='app_catalog.category', verbose_name='Category')),
            ],
            options={
                'verbose_name': 'Subcategory',
                'verbose_name_plural': 'Subcategories',
            },
        ),
        migrations.CreateModel(
            name='ProductSpecification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('value', models.CharField(max_length=255, verbose_name='Value')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='specifications', to='app_catalog.product', verbose_name='Product')),
            ],
            options={
                'verbose_name': 'Specification',
                'verbose_name_plural': 'Specifications',
            },
        ),
        migrations.CreateModel(
            name='ProductReview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, verbose_name='Email')),
                ('text', models.TextField(verbose_name='Text')),
                ('rate', models.IntegerField(verbose_name='Rate')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='Date')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Author')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='app_catalog.product', verbose_name='Product')),
            ],
            options={
                'verbose_name': 'Review',
                'verbose_name_plural': 'Reviews',
            },
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('src', models.ImageField(upload_to=app_catalog.models.product_directory, verbose_name='Source')),
                ('alt', models.CharField(max_length=255, verbose_name='Alt')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='app_catalog.product', verbose_name='Product')),
            ],
            options={
                'verbose_name': 'Image',
                'verbose_name_plural': 'Images',
            },
        ),
    ]