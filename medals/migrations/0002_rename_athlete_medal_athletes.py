# Generated by Django 3.2.7 on 2021-10-02 05:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('medals', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='medal',
            old_name='athlete',
            new_name='athletes',
        ),
    ]
