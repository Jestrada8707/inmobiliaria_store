from django import forms
from django.shortcuts import render
from django_extensions.db.fields import AutoSlugField
from django.db import models
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.core.validators import RegexValidator

from modelcluster.fields import ParentalKey, ParentalManyToManyField

from wagtail.core.models import Page, Orderable
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel, InlinePanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.core.fields import RichTextField
from wagtail.snippets.models import register_snippet
from wagtail.contrib.routable_page.models import RoutablePageMixin, route


class ListadoPropiedades(RoutablePageMixin, Page):
    """ Listado de propiedades. """

    template = "house/list_homes.html"
    max_count = 1

    lista_propiedades = models.CharField(
        max_length=130,
        blank=False,
        null=False,
        help_text='Titulo principal para el listado de la seccion. Ejemplo: Apartamentos, Casas, Lotes, Fincas, Aparta Estudios',

    )

    content_panels = Page.content_panels + [
        FieldPanel('lista_propiedades'),
    ]

    def get_context(self, request, *args, **kwargs):
        """Añadiendo cosas personalizadas a nuestro contexto"""

        context = super().get_context(request, *args, **kwargs)
        detail_pages = AgregarPropiedad.objects.live().public().order_by('-first_published_at')

        paginator = Paginator(detail_pages, 12)

        page = request.GET.get('page')

        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)

        context['posts'] = posts
        context["categoria"] = Categorias.objects.all()
        context["mercado"] = Mercados.objects.all()
        context["ubicacion"] = Ubicaciones.objects.all()
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

    @route(r'^market/(?P<market_slug>[-\w]*)/$', name="market_view")
    def market_view(self, request, market_slug):
        """Encontrar publicaciones por mercado"""

        context = self.get_context(request)

        try:
            market = Mercados.objects.get(slug=market_slug)

        except Mercados.DoesNotExist:
            return render(request, "house/market_not_found.html")

        context["posts"] = AgregarPropiedad.objects.live().public().filter(mercado__in=[market])
        return render(request, "house/market_filter_page.html", context)

    @route(r'^location/(?P<location_slug>[-\w]*)/$', name="location_view")
    def location_view(self, request, location_slug):
        """Encontrar publicaciones por locacion"""

        context = self.get_context(request)

        try:
            location = Ubicaciones.objects.get(slug=location_slug)

        except Mercados.DoesNotExist:
            return render(request, "house/location_not_found.html")

        context["posts"] = AgregarPropiedad.objects.live().public().filter(ubicacion__in=[location])
        return render(request, "house/location_filter_page.html", context)


class AgregarPropiedad(Page):
    """Caracteristicas del inmueble, titulo, antiguedad, precio, fotos, descripcion, telefono del vendedor """

    template = "house/home_detail_page.html"

    titulo_inmueble = models.CharField(
        max_length=120,
        blank=False,
        null=False,
        help_text='Titulo principal del inmueble. '
    )

    precio_inmueble = models.CharField(
        blank=False,
        null=True,
        max_length=10,
        validators=[RegexValidator(r'^\d{1,10}$')],
        help_text='Precio del inmueble'

    )

    mercado = ParentalManyToManyField("house.Mercados", blank=False)

    categoria = ParentalManyToManyField("house.Categorias", blank=False)

    ubicacion = ParentalManyToManyField("house.Ubicaciones", blank=False)

    area_inmueble = models.CharField(
        blank=True,
        null=True,
        max_length=5,
        validators=[RegexValidator(r'^\d{1,10}$')],
        help_text='Area del inmueble'

    )

    numero_habitaciones = models.CharField(
        blank=True,
        null=True,
        max_length=2,
        validators=[RegexValidator(r'^\d{1,10}$')],
        help_text='Habitaciones disponibles'
    )
    numero_banos = models.CharField(
        blank=True,
        null=True,
        max_length=1,
        validators=[RegexValidator(r'^\d{1,10}$')],
        help_text='Numero de baños'
    )
    numero_contacto = models.CharField(
        blank=False,
        null=False,
        max_length=10,
        validators=[RegexValidator(r'^\d{1,10}$')],
        help_text='Numero de baños'
    )
    antiguedad_del_inmueble = models.CharField(
        blank=True,
        null=True,
        max_length=4,
        validators=[RegexValidator(r'^\d{1,10}$')],
        help_text='Antiguedad o año de Construccion'

    )

    barrio = models.CharField(
        blank=True,
        null=True,
        max_length=100,
        help_text='Barrio'

    )

    fecha_publicacion = models.DateField(auto_now_add=True)

    descripcion_inmueble = RichTextField(
        blank=True,
        max_length=1000,
        features=['bold', 'italic']
    )

    def main_image(self):
        gallery_item = self.imagenes_inmueble.first()
        if gallery_item:
            return gallery_item.imagen_inmueble
        else:
            return None

    def resumen(self):
        return self.descripcion_inmueble[:200]

    def titulo_corto(self):
        return self.titulo_inmueble[:40]

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('titulo_inmueble'),
            FieldPanel('mercado', widget=forms.CheckboxSelectMultiple),
            FieldPanel('categoria', widget=forms.CheckboxSelectMultiple),
            FieldPanel('ubicacion', widget=forms.CheckboxSelectMultiple),
            FieldPanel('precio_inmueble'),
            FieldPanel('area_inmueble'),
            FieldPanel('numero_habitaciones'),
            FieldPanel('numero_banos'),
            FieldPanel('numero_contacto'),
            FieldPanel('antiguedad_del_inmueble'),
            FieldPanel('barrio'),
            FieldPanel('descripcion_inmueble'),
        ], heading='Datos del inmueble'),
        MultiFieldPanel([
            InlinePanel('imagenes_inmueble', max_num=12, min_num=1, label='Imagen Inmueble'),
        ], heading='Fotos del inmueble'),
    ]

    parent_page_types = ['house.ListadoPropiedades']


class ImagenesInmueble(Orderable):
    """ Imagenes del inmueble entre 1 y 12."""

    page = ParentalKey("AgregarPropiedad", related_name="imagenes_inmueble")
    imagen_inmueble = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    texto_imagen = models.CharField(blank=True, max_length=200)

    panels = [
        ImageChooserPanel("imagen_inmueble"),
        FieldPanel('texto_imagen'),
    ]


class Categorias(models.Model):
    nombre_categoria = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from='nombre_categoria', editable=True)
    icono = models.ForeignKey(
        'wagtailimages.Image', null=True, blank=True,
        on_delete=models.SET_NULL, related_name='+'
    )

    panels = [
        FieldPanel('nombre_categoria'),
        FieldPanel('slug'),
        ImageChooserPanel('icono'),
    ]

    def __str__(self):
        return self.nombre_categoria

    class Meta:
        verbose_name_plural = 'Categorias Inmuebles'
        ordering = ["nombre_categoria"]


register_snippet(Categorias)


class Mercados(models.Model):
    nombre_mercado = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from='nombre_mercado', editable=True)
    icono = models.ForeignKey(
        'wagtailimages.Image', null=True, blank=True,
        on_delete=models.SET_NULL, related_name='+'
    )

    panels = [
        FieldPanel('nombre_mercado'),
        FieldPanel('slug'),
        ImageChooserPanel('icono'),
    ]

    def __str__(self):
        return self.nombre_mercado

    class Meta:
        verbose_name_plural = 'Mercados Inmuebles'
        ordering = ["nombre_mercado"]


register_snippet(Mercados)


class Ubicaciones(models.Model):
    nombre_ubicacion = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from='nombre_ubicacion', editable=True)

    panels = [
        FieldPanel('nombre_ubicacion'),
        FieldPanel('slug'),
    ]

    def __str__(self):
        return self.nombre_ubicacion

    class Meta:
        verbose_name_plural = 'Ubicaciones'
        ordering = ["nombre_ubicacion"]


register_snippet(Ubicaciones)
