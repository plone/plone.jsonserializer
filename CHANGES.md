Changelog
=========

0.9.9 (2020-05-05)
------------------

- Python 3 compatibility [cdw9]


0.9.8 (2020-01-28)
------------------

Bug fixes:

- Fix unicode issue in deserializing RichTextValue from JSON [espenmn]

0.9.7 (2019-02-10)
------------------

- Python 3 compatibility
  [petschki]

0.9.6 (2017-12-14)
------------------

- Fix issue where deserialized rich text value got wrong default output
  mimetype (got "x-safe-html" instead of "x-html-safe")
  [datakurre]

0.9.5 (2017-08-30)
------------------

- Fix issue where invalid vocabulary value broke serialization by only warn
  about it and deserializing invalid value to None
  [datakurre]

0.9.4 (2017-08-21)
------------------

- Add support for serializing plone.app.textfield RichTextValues
  [datakurre]

0.9.3 (2017-04-24)
------------------

- Fix issue where schema_compatible was unable to deserializer BytesLine from unicode string
  [datakurre]


0.9.2 (2017-01-24)
------------------

- Fix issue where deserializer failed when value had extra fields to target
  schema
  [datakurre]


0.9.1 (2016-09-09)
------------------

- Add zope.schema.Bool adapter for ISchemaCompatible
  [datakurre]


0.9.0 (2016-09-08)
------------------

- First release.
