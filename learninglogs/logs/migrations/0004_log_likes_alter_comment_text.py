# Generated by Django 4.1.4 on 2023-01-23 18:33

import ckeditor_uploader.fields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logs', '0003_alter_group_description_alter_log_text_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='log',
            name='likes',
            field=models.ManyToManyField(blank=True, related_name='likes', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='comment',
            name='text',
            field=ckeditor_uploader.fields.RichTextUploadingField(),
        ),
    ]
