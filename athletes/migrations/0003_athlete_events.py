# Generated by Django 3.2.7 on 2021-10-02 08:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0003_auto_20211001_1839'),
        ('athletes', '0002_auto_20210930_1803'),
    ]

    operations = [
        migrations.AddField(
            model_name='athlete',
            name='events',
            field=models.ManyToManyField(related_name='athletes', to='games.Event'),
        ),
    ]