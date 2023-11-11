# Generated by Django 4.2.5 on 2023-10-17 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Created At'),
        ),
        migrations.AlterField(
            model_name='category',
            name='title',
            field=models.TextField(unique=True, verbose_name='Category Title'),
        ),
        migrations.AlterField(
            model_name='category',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Last Updated At'),
        ),
    ]