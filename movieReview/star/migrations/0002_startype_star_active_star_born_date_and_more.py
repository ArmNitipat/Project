# Generated by Django 4.2.5 on 2023-10-31 09:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('star', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='StarType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.AddField(
            model_name='star',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='star',
            name='born_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='star',
            name='born_location',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='star',
            name='died_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='star',
            name='died_location',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='star',
            name='height',
            field=models.FloatField(blank=True, default=0, help_text='height in meters.'),
        ),
        migrations.AddField(
            model_name='star',
            name='history',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='star',
            name='update_time',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.CreateModel(
            name='StarImageURL',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_url', models.URLField(max_length=2000)),
                ('active', models.BooleanField(default=True, verbose_name='Is Active')),
                ('star', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='star.star')),
            ],
        ),
        migrations.CreateModel(
            name='StarImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='stars/')),
                ('mainimage', models.BooleanField(default=False, verbose_name='Is Main')),
                ('active', models.BooleanField(default=True, verbose_name='Is Active')),
                ('star', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='star.star')),
            ],
        ),
        migrations.CreateModel(
            name='Spouses',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('marriage_date', models.DateField()),
                ('divorce', models.BooleanField(default=False)),
                ('spouse', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='spouse_star', to='star.star')),
                ('star', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='star.star')),
            ],
        ),
        migrations.CreateModel(
            name='Relatives',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('relative_name', models.CharField(max_length=255)),
                ('relationship', models.CharField(max_length=255)),
                ('star', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='star.star')),
            ],
        ),
        migrations.CreateModel(
            name='OtherWorks',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('work_description', models.TextField()),
                ('star', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='star.star')),
            ],
        ),
        migrations.CreateModel(
            name='Official_sites',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_site', models.CharField(max_length=100)),
                ('Official_sites', models.URLField(max_length=2000)),
                ('star', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='star.star')),
            ],
        ),
        migrations.CreateModel(
            name='Children',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('child_name', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='children_star', to='star.star')),
                ('star', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='star.star')),
            ],
        ),
        migrations.CreateModel(
            name='AlternativeNames',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('alternative_name', models.CharField(max_length=100)),
                ('star', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='star.star')),
            ],
        ),
        migrations.AddField(
            model_name='star',
            name='job',
            field=models.ManyToManyField(blank=True, related_name='stars', to='star.startype'),
        ),
    ]
