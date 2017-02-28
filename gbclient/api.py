from app import app
from flask import jsonify, abort

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
