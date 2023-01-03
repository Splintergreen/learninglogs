# Generated by Django 4.1.4 on 2022-12-30 18:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logs', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('logs', models.ManyToManyField(related_name='groups', to='logs.log')),
            ],
        ),
    ]
