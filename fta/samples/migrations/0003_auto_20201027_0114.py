# Generated by Django 3.0.10 on 2020-10-27 06:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('samples', '0002_sample_freeze_software'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sample',
            name='frozen_page',
            field=models.TextField(verbose_name='Blob of freeze-dried page'),
        ),
    ]