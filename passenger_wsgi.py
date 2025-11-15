import os
import sys

# ЗАМЕНИТЕ username НА ВАШЕ ИМЯ ПОЛЬЗОВАТЕЛЯ
INTERP = os.path.expanduser("~/virtualenv/maksudov/3.12/bin/python3.12_bin")
if sys.executable != INTERP:
    os.execl(INTERP, INTERP, *sys.argv)

sys.path.insert(0, os.path.expanduser('~/maksudov'))
sys.path.insert(0, os.path.expanduser('~/virtualenv/maksudov/3.12/lib/python3.12/site-packages'))

os.environ['DJANGO_SETTINGS_MODULE'] = 'maksudov_project.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
