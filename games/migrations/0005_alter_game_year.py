# Generated by Django 3.2.7 on 2021-10-05 04:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0004_auto_20211005_0314'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='year',
            field=models.PositiveIntegerField(unique=True),
        ),
    ]