# Generated by Django 4.1.4 on 2022-12-30 19:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logs', '0006_alter_group_options_alter_log_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='log',
            options={'ordering': ['date_added'], 'verbose_name': 'Заметка', 'verbose_name_plural': 'Заметки'},
        ),
        migrations.AlterField(
            model_name='group',
            name='logs',
            field=models.ManyToManyField(blank=True, related_name='groups', to='logs.log'),
        ),
    ]