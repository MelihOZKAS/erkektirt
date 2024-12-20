# Generated by Django 5.0.6 on 2024-06-12 22:27

import tinymce.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("isimler", "0003_remove_post_sosyaldik_post_post_turu_post_post_type"),
    ]

    operations = [
        migrations.RemoveField(model_name="post", name="content",),
        migrations.AddField(
            model_name="post",
            name="icerik1",
            field=tinymce.models.HTMLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="post",
            name="icerik2",
            field=tinymce.models.HTMLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="post",
            name="icerik3",
            field=tinymce.models.HTMLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="post",
            name="icerik4",
            field=tinymce.models.HTMLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="post",
            name="icerik5",
            field=tinymce.models.HTMLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="post",
            name="icerik6",
            field=tinymce.models.HTMLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="post",
            name="icerik7",
            field=tinymce.models.HTMLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="post",
            name="sss",
            field=models.TextField(blank=True, null=True),
        ),
    ]
