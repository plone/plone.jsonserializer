# -*- coding: utf-8 -*-
from plone.jsonserializer.interfaces import ISchemaCompatible
from zope.component import adapter
from zope.component import ComponentLookupError
from zope.component import getMultiAdapter
from zope.interface import implementer
from zope.interface import Interface
from zope.schema._bootstrapinterfaces import IFromUnicode
from zope.schema.interfaces import IDict
from zope.schema.interfaces import IBool
from zope.schema.interfaces import IField
from zope.schema.interfaces import IFrozenSet
from zope.schema.interfaces import IList
from zope.schema.interfaces import ISet
from zope.schema.interfaces import ITuple
import logging

logger = logging.getLogger('plone.jsonserializer')


def schema_compatible(value, schema_or_field):
    """The schema_compatible function converts any value to zope.schema
    compatible data when possible, raising a TypeError for unsupported values.
    This is done by using the ISchemaCompatible converters.
    """
    if value is None:
        return value

    try:
        return getMultiAdapter((value, schema_or_field), ISchemaCompatible)
    except ComponentLookupError:
        logger.error((u'Deserializer not found for field type '
                      u'"{0:s}" with value "{1:s}" and it was '
                      u'deserialized to None.').format(
            schema_or_field, value))
        return None


@adapter(dict, Interface)
@implementer(ISchemaCompatible)
def schema_dict_converter(value, schema):
    if value == {}:
        return {}

    items = [(k, v) for k, v in value.items() if k in schema]
    keys, values = zip(*items)
    keys = map(str, keys)
    values = [schema_compatible(values[idx], schema[keys[idx]])
              for idx in range(len(keys))]
    return dict(zip(keys, values))


@adapter(Interface, IField)
@implementer(ISchemaCompatible)
def default_converter(value, field):
    return value


@adapter(Interface, IBool)
@implementer(ISchemaCompatible)
def bool_converter(value, field):
    return bool(value)


@adapter(Interface, IFromUnicode)
@implementer(ISchemaCompatible)
def from_unicode_converter(value, field):
    return field.fromUnicode(value)


@adapter(list, IList)
@implementer(ISchemaCompatible)
def list_converter(value, field):
    return [schema_compatible(item, field.value_type)
            for item in value]


@adapter(list, ITuple)
@implementer(ISchemaCompatible)
def tuple_converter(value, field):
    return tuple(list_converter(value, field))


@adapter(list, ISet)
@implementer(ISchemaCompatible)
def set_converter(value, field):
    return set(list_converter(value, field))


@adapter(list, IFrozenSet)
@implementer(ISchemaCompatible)
def frozenset_converter(value, field):
    return frozenset(list_converter(value, field))


@adapter(dict, IDict)
@implementer(ISchemaCompatible)
def dict_converter(value, field):
    if value == {}:
        return {}

    keys, values = zip(*value.items())
    keys = [schema_compatible(keys[idx], field.key_type)
            for idx in range(len(keys))]
    values = [schema_compatible(values[idx], field.value_type)
              for idx in range(len(values))]
    return dict(zip(keys, values))
