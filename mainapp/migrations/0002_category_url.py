# Generated by Django 4.0.2 on 2022-02-09 04:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='url',
            field=models.SlugField(blank=True, max_length=100, null=True, unique=True, verbose_name='url'),
        ),
    ]
