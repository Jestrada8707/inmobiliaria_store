# Generated by Django 4.0.7 on 2022-11-16 22:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailimages', '0024_index_image_file_hash'),
        ('house', '0002_listadopropiedades_imagen_banner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imagenesinmueble',
            name='imagen_inmueble',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='wagtailimages.image'),
        ),
    ]