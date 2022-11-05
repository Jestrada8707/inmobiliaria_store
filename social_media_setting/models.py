from django.db import models

from wagtail.contrib.settings.models import BaseSetting, register_setting
from wagtail.admin.edit_handlers import MultiFieldPanel, FieldPanel


@register_setting
class SocialMedia(BaseSetting):
    """Social Media Data """

    facebook = models.URLField(
        blank=True,
        null=True,
        max_length=100,
        help_text='Coloque aqui la url de su pagina en Facebook'
    )

    instagram = models.URLField(
        blank=True,
        null=True,
        max_length=100,
        help_text='Coloque aqui la url de su perfil en Instagram'
    )

    youtube = models.URLField(
        blank=True,
        null=True,
        max_length=100,
        help_text='Coloque aqui la url de su canal en YouTube'
    )

    panels = [
        MultiFieldPanel([
            FieldPanel("facebook"),
            FieldPanel("instagram"),
            FieldPanel("youtube"),
        ], heading='Redes Sociales')
    ]
