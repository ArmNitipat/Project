# Generated by Django 4.2.5 on 2023-10-31 13:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('adminHome', '0009_delete_star_delete_starimage_delete_starimageurl_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Premium',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('price', models.DecimalField(decimal_places=2, max_digits=8, verbose_name='Price')),
                ('num', models.PositiveIntegerField(verbose_name='Number')),
                ('imag', models.ImageField(upload_to='premium_images/', verbose_name='Image')),
                ('date', models.DateField(verbose_name='Date')),
                ('expires', models.DateField(verbose_name='Expires')),
            ],
        ),
        migrations.CreateModel(
            name='Premium_list',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('premium', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='adminHome.premium', verbose_name='Premium Product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name': 'Product List',
                'verbose_name_plural': 'Product Lists',
            },
        ),
    ]
