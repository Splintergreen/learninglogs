# Generated by Django 4.1.4 on 2023-01-03 17:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('logs', '0010_group_owner'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='group',
            name='owner',
        ),
    ]