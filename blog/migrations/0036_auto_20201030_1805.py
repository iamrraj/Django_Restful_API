# Generated by Django 2.2.13 on 2020-10-30 18:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0035_auto_20201030_1804'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='key',
            field=models.CharField(default='1b21f40a8873599bd363', max_length=255, verbose_name='Key for email tracking'),
        ),
    ]