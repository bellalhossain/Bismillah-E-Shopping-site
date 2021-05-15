# Generated by Django 2.2.14 on 2021-05-07 10:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ecom', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=200, unique=True)),
                ('slug', models.SlugField(blank=True, max_length=200, null=True, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=254, unique=True)),
                ('description_heading_one', models.CharField(blank=True, max_length=254, null=True)),
                ('description_one', models.TextField(blank=True, null=True)),
                ('description_heading_two', models.CharField(blank=True, max_length=254, null=True)),
                ('description_two', models.TextField(blank=True, null=True)),
                ('description_heading_three', models.CharField(blank=True, max_length=254, null=True)),
                ('description_three', models.TextField(blank=True, null=True)),
                ('price', models.DecimalField(decimal_places=2, default=0.0, max_digits=6)),
                ('image', models.ImageField(blank=True, null=True, upload_to='images')),
                ('graphics', models.CharField(blank=True, max_length=50, null=True)),
                ('processor', models.CharField(blank=True, max_length=50, null=True)),
                ('ram', models.CharField(blank=True, max_length=50, null=True)),
                ('screen', models.CharField(blank=True, max_length=50, null=True)),
                ('battery_life', models.CharField(blank=True, max_length=50, null=True)),
                ('slug', models.SlugField(blank=True, max_length=200, null=True, unique=True)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ecom.Category')),
            ],
        ),
    ]
