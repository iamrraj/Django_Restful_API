# Generated by Django 2.2.8 on 2020-10-23 11:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0029_auto_20201023_1107'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='key',
            field=models.CharField(default='23a98d29e03218a27f8a', max_length=255, verbose_name='Key for email tracking'),
        ),
    ]
