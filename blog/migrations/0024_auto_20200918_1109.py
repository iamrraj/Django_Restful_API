# Generated by Django 2.2.8 on 2020-09-18 11:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0023_auto_20200911_2000'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blogphoto',
            name='created_by',
        ),
        migrations.AlterField(
            model_name='blog',
            name='key',
            field=models.CharField(default='a5c139e5857c98f60db8', max_length=255, verbose_name='Key for email tracking'),
        ),
    ]