# Generated by Django 3.2.7 on 2021-10-05 17:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medals', '0002_rename_athlete_medal_athletes'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='medal',
            index=models.Index(fields=['medal_class'], name='medals_meda_medal_c_7915ac_idx'),
        ),
    ]
