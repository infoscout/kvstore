# Key-Value Store

App allows you to easily tag a django db object with key/value pairs.

## Implementation

### Setting up a django model with a kvstore

Setup a model with a kvstore by simply including the `register` method which appends a `kvstore` attribute to the model.

    # models.py
    import kvstore

    class Charity(models.Model):
      ...

    kvstore.register(Charity)

### Storing key/value tags

    charity = Charity.objects.get(pk=123)
    charity.kvstore.set('foo','bar')

    # Or set multiple key/values with a dictionary
    charity.kvstore.set({'foo': 'bar'})

### Returning key/value tags

    # Getting a single value
    value = charity.kvstore.get('foo') # prints 'bar'

    # Getting all key/values
    tags = charity.kvstore.all() # returns dict of all tags

    # You can also easily check if a key exists
    exists = charity.kvstore.has('foo')

### Deleting key/value tags

    # Delete single tag
    charity.kvstore.delete('foo')

    # Delete multiple tags
    charity.kvstore.delete(['foo','foo2'])

    # Delete all
    charity.kvstore.delete_all()

### Adding kvstore to admin

To add a kvstore to modeladmin, just requires one line:

    # model_admins.py
    from kvstore.model_admin import TagInline

    class CharityModelAdmin(ModelAdmin):
      inlines = [TagInline]
      ...

### Other queries

Note you can directly query the tag model as well. For example, if you want to get all objects that contain a key:

    # All charity tags with a 'pilot' tag
    ctype = ContentType.objects.get_for_model(Charity)
    tags = Tag.objects.filter(content_type=ctype, key='pilot').all()

## Future enhancements

Built-in support for JSON as a value

(testing)
