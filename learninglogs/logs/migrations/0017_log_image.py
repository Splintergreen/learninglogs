# Generated by Django 4.1.4 on 2023-01-11 23:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logs', '0016_remove_group_logs_group_logs'),
    ]

    operations = [
        migrations.AddField(
            model_name='log',
            name='image',
            field=models.ImageField(blank=True, upload_to='posts/', verbose_name='Картинка'),
        ),
    ]