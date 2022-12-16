# Generated by Django 4.1.4 on 2022-12-16 02:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0007_project_spotify_uri_delete_spotifymusic"),
    ]

    operations = [
        migrations.AlterField(
            model_name="project",
            name="spotify_uri",
            field=models.CharField(max_length=256),
        ),
        migrations.AlterField(
            model_name="project",
            name="top_image_url",
            field=models.URLField(max_length=256),
        ),
        migrations.AlterField(
            model_name="project",
            name="top_text",
            field=models.CharField(max_length=32),
        ),
    ]