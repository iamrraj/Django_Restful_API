# Generated by Django 2.2.8 on 2020-08-02 10:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0015_auto_20200802_1023'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='publish',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='blog',
            name='key',
            field=models.CharField(default='26bd07ac6d93712308ec', max_length=255, verbose_name='Key for email tracking'),
        ),
    ]