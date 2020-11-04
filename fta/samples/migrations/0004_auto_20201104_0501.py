# Generated by Django 3.0.10 on 2020-11-04 11:01

from django.db import migrations


def rename_singlepage_to_singlefile(apps, schema_editor):
    Sample = apps.get_model('samples', 'Sample')
    affected = Sample.objects.filter(freeze_software__exact='SinglePage')
    for sample in affected:
        sample.freeze_software = 'SingleFile'
    Sample.objects.bulk_update(affected, ['freeze_software'])


class Migration(migrations.Migration):

    dependencies = [
        ('samples', '0003_auto_20201101_0007'),
    ]

    operations = [
        migrations.RunPython(rename_singlepage_to_singlefile)
    ]