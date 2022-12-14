# Generated by Django 4.0.7 on 2022-11-04 23:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('wagtailcore', '0069_log_entry_jsonfield'),
    ]

    operations = [
        migrations.CreateModel(
            name='SocialMedia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('facebook', models.URLField(blank=True, help_text='Coloque aqui la url de su pagina en Facebook', max_length=100, null=True)),
                ('instagram', models.URLField(blank=True, help_text='Coloque aqui la url de su perfil en Instagram', max_length=100, null=True)),
                ('youtube', models.URLField(blank=True, help_text='Coloque aqui la url de su canal en YouTube', max_length=100, null=True)),
                ('site', models.OneToOneField(editable=False, on_delete=django.db.models.deletion.CASCADE, to='wagtailcore.site')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
