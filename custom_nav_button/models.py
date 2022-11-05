from django.db import models

from django_extensions.db.fields import AutoSlugField  # install django-extensions
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from wagtail.admin.edit_handlers import (
    MultiFieldPanel,
    InlinePanel,
    FieldPanel,
    PageChooserPanel
)
from wagtail.core.models import Orderable
from wagtail.snippets.models import register_snippet


class NavbarButton(Orderable):
    """Custom navbar button add model"""

    page = ParentalKey('CustomNav', related_name="nav_button")

    titulo_boton = models.CharField(
        blank=False,
        null=True,
        max_length=50
    )
    url_externa = models.CharField(
        max_length=500,
        blank=True
    )

    url_interna = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        related_name='+',
        on_delete=models.CASCADE,
    )

    abrir_en_nueva_ventana = models.BooleanField(default=False, blank=True)

    panels = [
        FieldPanel('titulo_boton'),
        FieldPanel('url_externa'),
        PageChooserPanel('url_interna'),
        FieldPanel('abrir_en_nueva_ventana'),
    ]

    @property
    def link(self):
        if self.url_interna:
            return self.url_interna.url
        elif self.url_externa:
            return self.url_externa
        return '#'

    @property
    def title(self):
        if self.url_interna and not self.titulo_boton:
            return self.url_interna.title
        elif self.titulo_boton:
            return self.titulo_boton
        return 'No hay titulo'


@register_snippet
class CustomNav(ClusterableModel):
    """The main menu"""

    titulo = models.CharField(max_length=100)
    slug = AutoSlugField(populate_from='titulo', editable=True)

    panels = [
        MultiFieldPanel([
            FieldPanel('titulo'),
            FieldPanel('slug'),
        ], heading='Botón para el navbar personalizado'),
        InlinePanel('nav_button', label='Boton personalizado navbar', max_num=3,
                    help_text="Máximo tres botones se pueden crear para la barra de navegación")
    ]

    def __str__(self):
        return self.titulo