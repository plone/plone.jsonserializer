# -*- coding: utf-8 -*-
import logging

from plone.jsonserializer.interfaces import ISchemaCompatible
from six.moves import range
from six.moves import zip
from zope.component import ComponentLookupError
from zope.component import adapter
from zope.component import getMultiAdapter
from zope.interface import Interface
from zope.interface import implementer
from zope.schema._bootstrapinterfaces import ConstraintNotSatisfied
from zope.schema._bootstrapinterfaces import IFromUnicode
from zope.schema.interfaces import IBool
from zope.schema.interfaces import IDict
from zope.schema.interfaces import IField
from zope.schema.interfaces import IFrozenSet
from zope.schema.interfaces import IList
from zope.schema.interfaces import ISet
from zope.schema.interfaces import ITuple

import six

try:
    from plone.app.textfield import IRichText
    from plone.app.textfield import RichTextValue
    HAS_RICH_TEXT_VALUE = True
except ImportError:
    HAS_RICH_TEXT_VALUE = False

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
        logger.warning((u'Deserializer not found for value '
                        u'"{0:s}" of field "{1:s}". '
                        u'Returning None instead.').format(
            value,
            schema_or_field.__name__
        ))
        return None


@adapter(dict, Interface)
@implementer(ISchemaCompatible)
def schema_dict_converter(value, schema):
    if value == {}:
        return {}

    items = [(k, v) for k, v in value.items() if k in schema]
    keys, values = list(zip(*items))
    keys = [str(k) for k in keys]
    values = [schema_compatible(values[idx], schema[keys[idx]])
              for idx in range(len(keys))]
    return dict(list(zip(keys, values)))


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
    try:
        return field.fromUnicode(value)
    except UnicodeEncodeError:
        return value.encode('utf-8', 'ignore')
    except ConstraintNotSatisfied:
        logger.warning(
            u'Constraint not satisfied for value '
            u'"{0:s}" of field "{1:s}". '
            u'Returning None instead.'.format(
                value,
                field.__name__
            ))
        return None


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

    keys, values = list(zip(*list(value.items())))
    keys = [schema_compatible(keys[idx], field.key_type)
            for idx in range(len(keys))]
    values = [schema_compatible(values[idx], field.value_type)
              for idx in range(len(values))]
    value = dict(list(zip(keys, values)))

    return value


if HAS_RICH_TEXT_VALUE:
    @adapter(dict, IRichText)
    @implementer(ISchemaCompatible)
    def richtext_converter(value, schema):
        encoding = value.get('encoding', u'utf-8')
        if not isinstance(encoding, six.text_type):
            encoding = encoding.decode('utf-8', 'ignore')
        raw = value.get('data', '')
        if not isinstance(raw, six.text_type):
            raw = raw.decode(encoding, 'ignore')
        mimeType = value.get('content-type', u'text/html')
        if not isinstance(mimeType, six.text_type):
            mimeType = mimeType.decode(encoding, 'ignore')
        outputMimeType = value.get('output-content-type', u'text/x-html-safe')
        if not isinstance(outputMimeType, six.text_type):
            outputMimeType = outputMimeType.decode(encoding, 'ignore')
        return RichTextValue(
            raw=raw,
            mimeType=mimeType,
            outputMimeType=outputMimeType,
            encoding=encoding
        )
