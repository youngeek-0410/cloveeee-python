# Generated by Django 4.1.3 on 2022-12-13 14:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0003_spotifymusic"),
    ]

    operations = [
        migrations.AddField(
            model_name="SpotifyMusic",
            name="music_uri",
            field=models.CharField(max_length=256),
        ),
    ]
