from app import app
from flask import jsonify, abort, request

import platform
import socket
import utils


@app.route('/api/v1/about', methods=['GET'])
def about():
    return jsonify({
        'version': '1.0',
        'api_version': '2',
        'platform': platform.system(),
        'hostname': socket.gethostname(),
        'printers': [printer for printer in utils.get_printers()]
    })


@app.route('/api/v1/printer', methods=['GET'])
def printer_list():
    return jsonify([printer for printer in utils.get_printers()])


@app.route('/api/v1/printer/<printer_name>', methods=['GET'])
def printer_get(printer_name):
    if not utils.printer_exists(printer_name):
        return abort(404)

    return jsonify(utils.get_printer(printer_name))


@app.route('/api/v1/printer/<printer_name>', methods=['POST'])
def printer_print(printer_name):
    if not utils.printer_exists(printer_name):
        return abort(404)

    if not request.is_json:
        return abort(400)

    context = request.json or {}
    label_name = context.pop('label')

    if label_name.startswith('static') or label_name == 'base':
        return abort(400)

    media_size, filename = utils.generate_pdf(label_name, context)
    utils.print_pdf(printer_name, filename, media_size)

    return ''
