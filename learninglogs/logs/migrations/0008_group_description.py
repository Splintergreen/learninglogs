# Generated by Django 4.1.4 on 2023-01-02 20:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logs', '0007_alter_log_options_alter_group_logs'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='description',
            field=models.TextField(default='some descriptions'),
            preserve_default=False,
        ),
    ]