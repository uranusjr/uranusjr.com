from .base import *     # NOQA


DEBUG = True
TEMPLATE_DEBUG = DEBUG
FILEBROWSER_DEBUG = DEBUG

SECRET_KEY = 'i=sp#p$s^dwm6etgercjjo4$0t77#^=!t6v4sb61ad+^tcy@)i'

STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), 'static')
MEDIA_ROOT = os.path.join(os.path.dirname(BASE_DIR), 'media')
