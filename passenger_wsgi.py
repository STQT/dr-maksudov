import os
import sys
from pathlib import Path
from typing import Final

# === НАСТРОЙТЕ ПОД СВОЙ ХОСТИНГ =========================================
# Укажите имя каталога проекта и виртуального окружения на сервере cPanel.
# Пример: /home/USERNAME/maksudov.uz
PROJECT_ROOT: Final[Path] = Path.home() / "maksudov.uz"
VENV_ROOT: Final[Path] = Path.home() / "virtualenv" / "website" / "3.12"
# =========================================================================

PYTHON_INTERP = VENV_ROOT / "bin" / "python3.12"

if sys.executable != str(PYTHON_INTERP):
    os.execl(str(PYTHON_INTERP), str(PYTHON_INTERP), *sys.argv)

sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(VENV_ROOT / "lib" / "python3.12" / "site-packages"))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "maksudov_project.settings")

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()

