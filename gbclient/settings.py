import os

DEBUG = True
PARENT_DIR = os.path.dirname(os.path.dirname(__file__))
TEMPLATE_FOLDER = os.path.join(PARENT_DIR, 'examples')

try:
    from local_settings import *
except:
    pass
