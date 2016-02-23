"""
WSGI config for wfan project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/howto/deployment/wsgi/
"""

import os,sys,site

# virtualenvのパッケージパス
site.addsitedir("/home/ec2-user/env001/lib/python3.4/site-packages")
site.addsitedir("/home/ec2-user/env001/lib64/python3.4/site-packages")
sys.path.append('/opt/python/current/app/wfan')
sys.path.append('/opt/python/current/app/wfan/wfan')

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "wfan.settings")

# virtualenvの実行コードのパス
exec(compile(open('/home/ec2-user/env001/bin/activate_this.py').read(), '/home/ec2-user/env001/bin/activate_this.py', 'exec'))

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()