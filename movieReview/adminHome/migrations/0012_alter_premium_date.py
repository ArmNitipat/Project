# Generated by Django 4.2.5 on 2023-10-31 13:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminHome', '0011_premium_title_alter_premium_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='premium',
            name='date',
            field=models.DateField(auto_now=True, verbose_name='Date'),
        ),
    ]