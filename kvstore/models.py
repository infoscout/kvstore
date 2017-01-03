from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.db import models

from kvstore.managers import TagManager


class Tag(models.Model):

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    key = models.CharField(max_length=32, null=False, blank=False, db_index=True)
    value = models.TextField(null=False)

    objects = TagManager()

    class Meta:
        # Enforce unique tag association per object
        unique_together = (('content_type', 'object_id', 'key'),)

    def __unicode__(self):
        return u'%s - %s - %s' % (self.content_object, self.key, self.value)
