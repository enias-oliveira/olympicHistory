# Generated by Django 3.2.7 on 2021-10-05 03:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0003_auto_20211001_1839'),
    ]

    operations = [
        migrations.AlterField(
            model_name='competition',
            name='name',
            field=models.CharField(max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='sport',
            name='name',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
