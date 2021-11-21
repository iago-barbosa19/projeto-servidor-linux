#
# Conteudo do arquivo `wsgi.py`
#
import sys

sys.path.insert(0, "/etc/psc")

from prototipoFlask import app as application