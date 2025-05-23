# Generated by Django 5.0.6 on 2024-06-13 21:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("isimler", "0007_allname"),
    ]

    operations = [
        migrations.RenameField(
            model_name="allname", old_name="Post_Turu", new_name="Durum",
        ),
        migrations.RenameField(
            model_name="allname", old_name="title", new_name="isim",
        ),
        migrations.AddField(
            model_name="allname",
            name="Cinsiyet",
            field=models.CharField(
                choices=[
                    ("Kız", "Kız"),
                    ("Erkek", "Erkek"),
                    ("Unisex", "Unisex"),
                    ("B", "B"),
                ],
                max_length=255,
                null=True,
            ),
        ),
    ]
