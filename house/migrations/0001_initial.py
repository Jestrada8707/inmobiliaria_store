# Generated by Django 4.0.7 on 2022-10-26 23:32

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields
import modelcluster.fields
import wagtail.contrib.routable_page.models
import wagtail.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('wagtailcore', '0069_log_entry_jsonfield'),
        ('wagtailimages', '0024_index_image_file_hash'),
    ]

    operations = [
        migrations.CreateModel(
            name='AgregarPropiedad',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
                ('titulo_inmueble', models.CharField(help_text='Titulo principal del inmueble. ', max_length=120)),
                ('precio_inmueble', models.CharField(help_text='Precio del inmueble', max_length=10, null=True, validators=[django.core.validators.RegexValidator('^\\d{1,10}$')])),
                ('area_inmueble', models.CharField(blank=True, help_text='Area del inmueble', max_length=5, null=True, validators=[django.core.validators.RegexValidator('^\\d{1,10}$')])),
                ('numero_habitaciones', models.CharField(blank=True, help_text='Habitaciones disponibles', max_length=2, null=True, validators=[django.core.validators.RegexValidator('^\\d{1,10}$')])),
                ('numero_banos', models.CharField(blank=True, help_text='Numero de baños', max_length=1, null=True, validators=[django.core.validators.RegexValidator('^\\d{1,10}$')])),
                ('numero_contacto', models.CharField(help_text='Numero de baños', max_length=10, validators=[django.core.validators.RegexValidator('^\\d{1,10}$')])),
                ('antiguedad_del_inmueble', models.CharField(blank=True, help_text='Antiguedad o año de Construccion', max_length=4, null=True, validators=[django.core.validators.RegexValidator('^\\d{1,10}$')])),
                ('barrio', models.CharField(blank=True, help_text='Barrio', max_length=100, null=True)),
                ('fecha_publicacion', models.DateField(auto_now_add=True)),
                ('descripcion_inmueble', wagtail.fields.RichTextField(blank=True, max_length=1000)),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='ListadoPropiedades',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
                ('lista_propiedades', models.CharField(help_text='Titulo principal para el listado de la seccion. Ejemplo: Apartamentos, Casas, Lotes, Fincas, Aparta Estudios', max_length=130)),
            ],
            options={
                'abstract': False,
            },
            bases=(wagtail.contrib.routable_page.models.RoutablePageMixin, 'wagtailcore.page'),
        ),
        migrations.CreateModel(
            name='Ubicaciones',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_ubicacion', models.CharField(max_length=255)),
                ('slug', django_extensions.db.fields.AutoSlugField(blank=True, editable=False, populate_from='nombre_ubicacion')),
            ],
            options={
                'verbose_name_plural': 'Ubicaciones',
                'ordering': ['nombre_ubicacion'],
            },
        ),
        migrations.CreateModel(
            name='Mercados',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_mercado', models.CharField(max_length=255)),
                ('slug', django_extensions.db.fields.AutoSlugField(blank=True, editable=False, populate_from='nombre_mercado')),
                ('icono', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image')),
            ],
            options={
                'verbose_name_plural': 'Mercados Inmuebles',
                'ordering': ['nombre_mercado'],
            },
        ),
        migrations.CreateModel(
            name='ImagenesInmueble',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('texto_imagen', models.CharField(blank=True, max_length=200)),
                ('imagen_inmueble', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image')),
                ('page', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='imagenes_inmueble', to='house.agregarpropiedad')),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Categorias',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_categoria', models.CharField(max_length=255)),
                ('slug', django_extensions.db.fields.AutoSlugField(blank=True, editable=False, populate_from='nombre_categoria')),
                ('icono', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image')),
            ],
            options={
                'verbose_name_plural': 'Categorias Inmuebles',
                'ordering': ['nombre_categoria'],
            },
        ),
        migrations.AddField(
            model_name='agregarpropiedad',
            name='categoria',
            field=modelcluster.fields.ParentalManyToManyField(to='house.categorias'),
        ),
        migrations.AddField(
            model_name='agregarpropiedad',
            name='mercado',
            field=modelcluster.fields.ParentalManyToManyField(to='house.mercados'),
        ),
        migrations.AddField(
            model_name='agregarpropiedad',
            name='ubicacion',
            field=modelcluster.fields.ParentalManyToManyField(to='house.ubicaciones'),
        ),
    ]
