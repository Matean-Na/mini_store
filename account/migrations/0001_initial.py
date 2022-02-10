# Generated by Django 4.0.2 on 2022-02-09 07:41

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TemporaryBanIp',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip_address', models.GenericIPAddressField(verbose_name='IP адрес')),
                ('attempts', models.IntegerField(default=0, verbose_name='Неудачных попыток')),
                ('time_unblock', models.DateTimeField(blank=True, verbose_name='Время разблокировки')),
                ('status', models.BooleanField(default=False, verbose_name='Статус блокировки')),
            ],
            options={
                'db_table': 'TemporaryBanIp',
            },
        ),
    ]
