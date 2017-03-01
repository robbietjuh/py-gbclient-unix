import cups
import os
import uuid
import html5lib

from flask import render_template
from xhtml2pdf import pisa

from settings import TEMPLATE_FOLDER

CUPS_CONN = cups.Connection()

PRINTER_ARGUMENTS = (
    ('printer-info', 'name'),
    ('printer-make-and-model', 'model'),
    ('printer-location', 'location'),
)


def get_printers():
    for cups_id, cups_details in CUPS_CONN.getPrinters().iteritems():
        details = {'id': cups_id}

        for cups_arg, json_arg in PRINTER_ARGUMENTS:
            details[json_arg] = cups_details[cups_arg]

        yield details


def printer_exists(printer_id):
    return printer_id in CUPS_CONN.getPrinters()


def get_printer(printer_id):
    for item in get_printers():
        if item['id'] == printer_id:
            return item


def generate_label_html(label_name, context):
    template = render_template('%s.html' % label_name, **context)
    return template


def get_media_size(template):
    parser = html5lib.HTMLParser(tree=html5lib.getTreeBuilder("dom"))
    doc = parser.parse(template)
    attr = doc.documentElement.attributes.get('data-gbclient-media-size')

    return attr.value if attr else '62mm'


def generate_pdf(label_name, context):
    template = generate_label_html(label_name, context)
    media_size = get_media_size(template)
    filename = '/tmp/%s.pdf' % uuid.uuid4()

    with open(os.path.join(filename), "w+b") as f:
        pisa.CreatePDF(template, dest=f, link_callback=lambda uri, _: '%s/%s' % (TEMPLATE_FOLDER, uri))

    return media_size, filename


def print_pdf(printer_name, filename, media_size):
    CUPS_CONN.printFile(printer_name, filename, 'gbclient-unix label', options={'media': media_size})
