# Generated by Django 4.1.4 on 2023-01-02 21:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logs', '0008_group_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='log',
            name='description',
            field=models.TextField(default='exit'),
            preserve_default=False,
        ),
    ]
