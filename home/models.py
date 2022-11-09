from django import forms
from django.db import models
from django.shortcuts import render
from django_extensions.db.fields import AutoSlugField

from modelcluster.fields import ParentalKey, ParentalManyToManyField

from wagtail.models import Page, Orderable
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.admin.edit_handlers import InlinePanel, MultiFieldPanel, FieldPanel, PageChooserPanel
from wagtail.core.fields import RichTextField
from wagtail.snippets.models import register_snippet

from wagtail.contrib.routable_page.models import RoutablePageMixin, route

from house.models import Categorias, AgregarPropiedad, ListadoPropiedades


class HomePage(RoutablePageMixin, Page):
    """Home page model"""
    template = "index/index.html"
    max_count = 1

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            InlinePanel('main_banner', max_num=1, min_num=1),
        ], heading='Título, texto y botón link para el banner principal. Debe al menos subir una imagen'),
        MultiFieldPanel([
            InlinePanel('banner_image', max_num=6, min_num=1),
        ],
            heading='Imágenes para el banner principal, se debe subir al menos una. Máximo 6 imágenes con título y link opcional '),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context['posts'] = AgregarPropiedad.objects.live().public().order_by('-first_published_at')[:6]
        context['categorias'] = Categorias.objects.all()
        context['banner_sell'] = BanerVenta.objects.all()
        context['list_page'] = ListadoPropiedades.objects.first()
        return context

    @route(r'^cat/(?P<cat_slug>[-\w]*)/$', name="category_view")
    def category_view(self, request, cat_slug):
        """Encontrar publicaciones por categoria"""

        context = self.get_context(request)

        try:
            category = Categorias.objects.get(slug=cat_slug)

        except Categorias.DoesNotExist:
            return render(request, "house/category_not_found.html")

        context["posts"] = AgregarPropiedad.objects.live().public().filter(categoria__in=[category])
        return render(request, "house/category_filter_page.html", context)


class BannerPrincipal(Orderable):
    """Imagenes y texto del banner principal"""

    page = ParentalKey("home.HomePage", related_name="main_banner")

    titulo_principal = models.CharField(
        max_length=45,
        blank=False,
        null=False,
        help_text="Titulo principal banner, no puede superar los 45 caracteres"
    )

    texto_principal = models.CharField(
        max_length=130,
        blank=True,
        null=True,
        help_text="Texto adicional, se puede usar para dar más información,no puede superar los 130 caracteres"
    )

    titulo_boton = models.CharField(
        null=True,
        blank=True,
        max_length=30,
        help_text="El título del botón no puede ser mayor a 30 caracteres"
    )

    url_link = models.URLField(
        max_length=500,
        blank=True,
        help_text="Pegue aquí la URL del sitio web,límite de 500 caracteres"
    )
    internal_link = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        related_name='+',
        on_delete=models.CASCADE,
        help_text="Selecciona una página de tu sitio para compartir en este botón"
    )

    abrir_nueva_ventana = models.BooleanField(
        default=False,
        blank=True,
        help_text="Active esta opción si desea que el link abra desde una ventana nueva"
    )

    @property
    def link(self):
        if self.internal_link:
            return self.internal_link.url
        elif self.url_link:
            return self.url_link
        return '#'

    panels = [
        FieldPanel('titulo_principal'),
        FieldPanel('texto_principal'),
        FieldPanel('titulo_boton'),
        FieldPanel('url_link'),
        PageChooserPanel('internal_link'),
        FieldPanel('abrir_nueva_ventana'),
    ]


class ImageCarousel(Orderable):
    page = ParentalKey("home.HomePage", related_name="banner_image")
    imagenes_carousel = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text="La imagen optima es de 1000px X 1000px"
    )

    titulo_imagen = models.CharField(
        max_length=30,
        blank=True,
        null=True,
        help_text="Su texto no puede superar los 30 caracteres"
    )

    url_link = models.URLField(
        max_length=500,
        blank=True,
        help_text="Pegue aquí la URL del sitio web,límite de 500 caracteres"
    )
    internal_link = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        related_name='+',
        on_delete=models.CASCADE,
    )

    abrir_nueva_ventana = models.BooleanField(
        default=False,
        blank=True,
        help_text="Active esta opción si desea que el link abra desde una ventana nueva"
    )

    @property
    def link(self):
        if self.internal_link:
            return self.internal_link.url
        elif self.url_link:
            return self.url_link
        return '#'

    panels = [
        ImageChooserPanel('imagenes_carousel'),
        FieldPanel('titulo_imagen'),
        FieldPanel('url_link'),
        PageChooserPanel('internal_link'),
        FieldPanel('abrir_nueva_ventana'),
    ]


class BanerVenta(Page):
    subpage_types = []
    parent_page_types = ['home.HomePage']
    imagen_banner = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text="La imagen optima es de 1000px X 1000px"
    )

    titulo_banner = models.CharField(
        max_length=70,
        blank=True,
        null=True,
        help_text="Su texto no puede superar los 70 caracteres"
    )

    texto_banner = RichTextField(
        blank=True,
        max_length=550,
        features=['bold', 'italic'],
        help_text='Escriba aquí el texto, máximo 550 caracteres'
    )

    requisitos = ParentalManyToManyField("home.RequisitosVenta", blank=True)

    titulo_boton = models.CharField(
        null=True,
        blank=True,
        max_length=30,
        help_text="Su texto no puede superar los 30 caracteres"
    )

    url_link = models.URLField(
        max_length=500,
        blank=True,
        help_text="Pegue aquí la URL del sitio web,límite de 500 caracteres"
    )
    internal_link = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        related_name='+',
        on_delete=models.SET_NULL,
    )

    abrir_nueva_ventana = models.BooleanField(
        default=False,
        blank=True,
        help_text="Active esta opción si desea que el link abra desde una ventana nueva"
    )

    @property
    def link(self):
        if self.internal_link:
            return self.internal_link.url
        elif self.url_link:
            return self.url_link
        return '#'

    content_panels = Page.content_panels + [
        ImageChooserPanel('imagen_banner'),
        FieldPanel('titulo_banner'),
        FieldPanel('texto_banner'),
        MultiFieldPanel(
            [
                FieldPanel('requisitos', widget=forms.CheckboxSelectMultiple),
            ], heading="Requisitos para publicar"
        ),
        FieldPanel('titulo_boton'),
        FieldPanel('url_link'),
        PageChooserPanel('internal_link'),
        FieldPanel('abrir_nueva_ventana'),
    ]


class RequisitosVenta(models.Model):
    requerimiento_venta = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from='requerimiento_venta', editable=True)

    panels = [
        FieldPanel('requerimiento_venta'),
        FieldPanel('slug'),
    ]

    def __str__(self):
        return self.requerimiento_venta

    class Meta:
        verbose_name_plural = 'Requisitos Venta'
        ordering = ["requerimiento_venta"]


register_snippet(RequisitosVenta)
