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


@app.route('/api/v1/printers', methods=['GET'])
def printers_list():
    try:
        return jsonify([printer for printer in utils.get_printers()])
    except:
        return abort(500)
