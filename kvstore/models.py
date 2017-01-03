from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.db import models


class TagManager(models.Manager):

    def tags(self, obj):
        """
        Returns dict of key/value tags for the object
        """
        ctype = ContentType.objects.get_for_model(obj)
        list = self.values_list('key', 'value').filter(
            content_type=ctype,
            object_id=obj.pk
        ).all()
        return dict(list)

    def tag(self, obj, key):
        """
        Returns value for a key related to the object
        """
        ctype = ContentType.objects.get_for_model(obj)
        try:
            tag = self.filter(content_type=ctype, object_id=obj.pk, key=key).get()
        except Tag.DoesNotExist:
            return None
        return tag.value

    def set(self, obj, key, value):
        """
        Sets a key/value. If none exists, creates record
        """
        ctype = ContentType.objects.get_for_model(obj)
        tag, created = self.get_or_create(
            content_type=ctype,
            object_id=obj.pk,
            key=key,
            defaults={'value': value}
        )
        tag.value = value  # If this tag already exists, get_or_create won't update the value
        tag.save()
        return tag

    def delete(self, obj, key):
        """
        Deletes specific key for a record
        """
        ctype = ContentType.objects.get_for_model(obj)
        self.filter(content_type=ctype, object_id=obj.pk, key=key).delete()

    def delete_all(self, obj):
        """
        Deletes all key/value records for an obj
        """
        ctype = ContentType.objects.get_for_model(obj)
        self.filter(content_type=ctype, object_id=obj.pk).delete()


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
