from kvstore.models import Tag


class TagAccessor(object):
    """
    An abstraction layer for the kvstore attached
    to the model.
    """

    def __init__(self, obj, cls):
        self.obj = obj
        self.cls = cls

    def set(self, arg1, arg2=None):
        """
        Saves key/value attributes to the database for an
        object. Can accept key, value as arguement or a
        dictionary to update multple. Example:

            obj.kvstore.set('foo', 'bar')
            obj.kvstore.set({'foo': 'bar'})
        """

        if not isinstance(arg1, dict):
            dict_set = {arg1: arg2}
        else:
            dict_set = arg1

        for k, v in dict_set.items():
            Tag.objects.set(self.obj, k, v)

    def delete(self, k):
        Tag.objects.delete(self.obj, k)

    def delete_all(self):
        Tag.objects.delete_all(self.obj)

    def get(self, k):
        return Tag.objects.tag(self.obj, k)

    def all(self):
        return Tag.objects.tags(self.obj)

    def has(self, k):
        tag = self.get(k)
        return tag is not None


class TagDescriptor(object):
    """
    A descriptor is attached to a model class.
    Provides access to a TagAccessor object which
    handles get, set, save of the kvstore.
    """

    def __get__(self, instance, owner):
        return TagAccessor(instance, owner)
