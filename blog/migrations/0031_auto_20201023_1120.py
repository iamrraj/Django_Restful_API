# Generated by Django 2.2.8 on 2020-10-23 11:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0030_auto_20201023_1110'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='key',
            field=models.CharField(default='20cdbde5fae6b2d8e70a', max_length=255, verbose_name='Key for email tracking'),
        ),
    ]