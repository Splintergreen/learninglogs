# Generated by Django 4.1.4 on 2023-01-30 20:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logs', '0006_delete_follow'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='logs',
            field=models.ManyToManyField(blank=True, related_name='groups', to='logs.log'),
        ),
    ]
