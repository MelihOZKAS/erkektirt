# Generated by Django 5.0.6 on 2024-06-18 21:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("isimler", "0014_remove_post_post_turu"),
    ]

    operations = [
        migrations.AddField(
            model_name="post",
            name="Post_Turu",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="isimler.postkategori",
            ),
        ),
    ]
