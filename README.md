# Key-Value Store

[![CircleCI](https://circleci.com/gh/infoscout/kvstore/tree/master.svg?style=svg)](https://circleci.com/gh/infoscout/kvstore/tree/master)
[![codecov](https://codecov.io/gh/infoscout/kvstore/branch/master/graph/badge.svg)](https://codecov.io/gh/infoscout/kvstore)

App allows you to easily tag a django db object with key/value pairs.

## Implementation

### Installation

1. Install package into Django runtime environment
1. Add `django.contrib.humanize` and `kvstore` to the list of `INSTALLED_APPS` in `settings.py` of your Django project
1. `python manage.py migrate`

### Setting up a django model with a kvstore

Setup a model with a kvstore by simply including the `register` method which appends a `kvstore` attribute to the model.

```python
# models.py
import kvstore

class Charity(models.Model):
  ...

kvstore.register(Charity)
```

### Storing key/value tags

```python
charity = Charity.objects.get(pk=123)
charity.kvstore.set('foo', 'bar')

# Or set multiple key/values with a dictionary
charity.kvstore.set({'foo': 'bar'})
```

### Returning key/value tags

```python
# Getting a single value
value = charity.kvstore.get('foo') # prints 'bar'

# Getting all key/values
tags = charity.kvstore.all() # returns dict of all tags

# You can also easily check if a key exists
exists = charity.kvstore.has('foo')
```

### Deleting key/value tags

```python
# Delete single tag
charity.kvstore.delete('foo')

# Delete multiple tags
charity.kvstore.delete(['foo', 'foo2'])

# Delete all
charity.kvstore.delete_all()
```

### Adding kvstore to ModelAdmin

To add a kvstore to `ModelAdmin`, just requires one line:

```python
# model_admins.py
from kvstore.model_admin import TagInline

class CharityModelAdmin(ModelAdmin):
  inlines = [TagInline]
  ...
```

### Adding Custom Tags View to Django Admin

```python
# admin.py
from kvstore.admin.admin import KVStoreAdminApp
from kvstore.models import Tag

admin.site.register(Tag, KVStoreAdminApp)
```

Custom view is available at `/admin/kvstore/tag/kvstore/upload`

### Other queries

Note you can directly query the tag model as well. For example, if you want to get all objects that contain a key:

```python
# All charity tags with a 'pilot' tag
ctype = ContentType.objects.get_for_model(Charity)
tags = Tag.objects.filter(content_type=ctype, key='pilot').all()
```

## Future enhancements

Built-in support for JSON as a value

## Contributing

### Setting up Development Environment

1. Create and activate virtual environment
1. `pip install -r requirements.txt`

### Running tests

```console
python setup.py test
```
