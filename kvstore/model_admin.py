from django.contrib.contenttypes.generic import GenericTabularInline
from django.db import models
from django.forms import widgets

from kvstore.models import Tag


class TagInline(GenericTabularInline):

    model = Tag
    formfield_overrides = {
        models.TextField: {'widget': widgets.TextInput},
    }
