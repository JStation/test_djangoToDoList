# wsgi for running django at testing.dishduty.com

import sys, os
cwd = os.getcwd()
sys.path.append(cwd)
sys.path.append(cwd + '/source')

os.environ['LD_LIBRARY_PATH'] = "/home/grak/testing.dishduty.com/virtualenv/lib"

INTERP = "/home/grak/testing.dishduty.com/virtualenv/bin/python"
if sys.executable != INTERP:
        os.execl(INTERP, INTERP, *sys.argv)

sys.path.insert(0, '/home/grak/testing.dishduty.com/virtualenv/bin')
sys.path.insert(0, '/home/grak/testing.dishduty.com/virtualenv/lib/python3.4/site-packages')
sys.path.insert(0, '/home/grak/testing.dishduty.com/virtualenv/lib')

os.environ['DJANGO_SETTINGS_MODULE'] = "superlists.settings"

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
