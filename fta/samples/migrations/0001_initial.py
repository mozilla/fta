# Generated by Django 3.0.10 on 2020-10-25 23:56

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Sample',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('frozen_page', models.BinaryField(editable=True, verbose_name='Blob of freeze-dried page')),
                ('url', models.URLField(max_length=1000, verbose_name='Url or frozen page')),
                ('freeze_time', models.DateTimeField(verbose_name='Time of page freezing')),
                ('notes', models.TextField(blank=True, null=True)),
            ],
        ),
    ]
