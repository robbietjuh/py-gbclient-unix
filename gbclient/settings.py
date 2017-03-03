import os
SETTINGS_PATH = os.path.abspath(__file__)
PARENT_DIR = os.path.dirname(os.path.dirname(SETTINGS_PATH))

DEBUG = True
TEMPLATE_FOLDER = os.path.join(PARENT_DIR, 'examples')

# Docs: http://flask-cors.corydolphin.com/en/latest/api.html
CORS_ENABLED = False
CORS_CONFIG = {
    'origins': ['localhost',],
}

try:
    from local_settings import *
except:
    pass
