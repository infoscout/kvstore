from kvstore.accessor import TagDescriptor


class AlreadyRegistered(Exception):
    """
    An attempt was made to register a model more than once.
    """
    pass


registry = []


def register(model, descriptor_attr='kvstore'):
    """
    Sets the given model class up for working with tags.
    """
    if model in registry:
        return

    if hasattr(model, descriptor_attr):
        raise AttributeError(
            "'%s' already has an attribute '%s'. You must provide a custom tag_descriptor_attr to register." % (
                model._meta.object_name,
                descriptor_attr,
            )
        )

    # Add tag descriptor
    setattr(model, descriptor_attr, TagDescriptor())

    # Finally register in registry
    registry.append(model)
