from django.db import models

from wagtail.models import Page


class HomePage(Page):
    """Home page model"""
    template = "index/index.html"
    max_count = 1
