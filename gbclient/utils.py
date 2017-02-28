import cups

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