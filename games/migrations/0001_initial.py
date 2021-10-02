# Generated by Django 3.2.7 on 2021-09-30 20:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Competition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('competition', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='games.competition')),
            ],
        ),
        migrations.CreateModel(
            name='Sport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(max_length=255)),
                ('year', models.PositiveIntegerField()),
                ('season', models.CharField(choices=[('S', 'Summer'), ('W', 'Winter')], max_length=6)),
                ('events', models.ManyToManyField(through='games.Event', to='games.Competition')),
            ],
        ),
        migrations.AddField(
            model_name='event',
            name='game',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='games.game'),
        ),
        migrations.AddField(
            model_name='competition',
            name='sport',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='competitions', to='games.sport'),
        ),
    ]