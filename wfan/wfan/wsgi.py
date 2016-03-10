import os
import sys
import site
from django.core.wsgi import get_wsgi_application
from django.core.wsgi import get_wsgi_application

# virtualenvのパッケージパス
site.addsitedir("/home/ec2-user/env001/lib/python3.4/site-packages")
site.addsitedir("/home/ec2-user/env001/lib64/python3.4/site-packages")
sys.path.append('/opt/python/current/app/wfan')
sys.path.append('/opt/python/current/app/wfan/wfan')

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "wfan.settings")

# virtualenvの実行コードのパス
exec(compile(open('/home/ec2-user/env001/bin/activate_this.py').read(),
             '/home/ec2-user/env001/bin/activate_this.py', 'exec'))

application = get_wsgi_application()
