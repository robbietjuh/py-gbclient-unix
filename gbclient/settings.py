import os

DEBUG = True
SETTINGS_PATH = os.path.abspath(__file__)
PARENT_DIR = os.path.dirname(os.path.dirname(SETTINGS_PATH))
TEMPLATE_FOLDER = os.path.join(PARENT_DIR, 'examples')

try:
    from local_settings import *
except:
    pass
