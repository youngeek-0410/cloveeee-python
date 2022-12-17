# Generated by Django 4.1.4 on 2022-12-17 01:06

import app.models.project
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0007_project_spotify_uri_delete_spotifymusic"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="project",
            name="top_image_url",
        ),
        migrations.AddField(
            model_name="project",
            name="top_image",
            field=models.ImageField(
                default=None,
                null=True,
                upload_to=app.models.project.upload_to_top_image,
            ),
        ),
    ]