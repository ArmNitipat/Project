# Generated by Django 4.2.5 on 2023-11-06 09:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0005_alter_localimage_star_alter_movie_director_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='time',
            field=models.CharField(blank=True, max_length=10, verbose_name='Movie Time'),
        ),
    ]
