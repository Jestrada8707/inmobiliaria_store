# Generated by Django 4.0.7 on 2022-11-08 20:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailimages', '0024_index_image_file_hash'),
        ('house', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='listadopropiedades',
            name='imagen_banner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image'),
        ),
    ]
