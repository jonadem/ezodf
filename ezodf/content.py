#!/usr/bin/env python
#coding:utf-8
# Author:  mozman --<mozman@gmx.at>
# Purpose: ODF content.xml document management
# Created: 28.12.2010
# Copyright (C) 2010, Manfred Moitzi
# License: GPLv3

from .const import MIMETYPE_NSMAP
from .xmlns import XMLMixin, subelement, CN, etree, register_class, wrap
from .base import GenericWrapper

class OfficeDocumentContent(XMLMixin):
    TAG = CN('office:document-content')

    def __init__(self, mimetype, xmlnode=None):

        if xmlnode is None:
            self.xmlnode = etree.Element(self.TAG, nsmap=MIMETYPE_NSMAP[mimetype])
        elif xmlnode.tag == self.TAG:
            self.xmlnode = xmlnode
        else:
            raise ValueError("Unexpected root node: %s" % xmlnode.tag)
        self._setup_references(mimetype)

    def _setup_references(self, mimetype):
        # these elements are common to all document types
        # The element office:scripts always exists but is always empty
        self.scripts = wrap(subelement(self.xmlnode, CN('office:scripts')))
        self.fonts = wrap(subelement(self.xmlnode, CN('office:font-face-decls')))
        self.automatic_styles = wrap(subelement(self.xmlnode, CN('office:automatic-styles')))
        self.body = wrap(subelement(self.xmlnode, CN('office:body')))

    def get_application_body(self, bodytag):
        # The office:body element is just frame element for the real document content:
        # office:text, office:spreadsheet, office:presentation, office:drawing
        return wrap(subelement(self.body.xmlnode, bodytag))

@register_class
class TextBody(GenericWrapper):
    TAG = CN('office:text')

@register_class
class SpreadsheetBody(GenericWrapper):
    TAG = CN('office:spreadsheet')

@register_class
class PresentationBody(GenericWrapper):
    TAG = CN('office:presentation')

@register_class
class DrawingBody(GenericWrapper):
    TAG = CN('office:drawing')

@register_class
class ChartBody(GenericWrapper):
    TAG = CN('office:chart')

@register_class
class ImageBody(GenericWrapper):
    TAG = CN('office:image')
