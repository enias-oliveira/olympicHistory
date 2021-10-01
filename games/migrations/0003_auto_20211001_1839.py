# Generated by Django 3.2.7 on 2021-10-01 18:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0002_rename_events_game_competitions'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='game',
            name='competitions',
        ),
        migrations.AddField(
            model_name='game',
            name='events',
            field=models.ManyToManyField(through='games.Event', to='games.Competition'),
        ),
    ]
