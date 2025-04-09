"""
WSGI config for myprojects project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myprojects.settings')

application = get_wsgi_application()


git init
git add .
git commit -m "initial commit"
git remote add origin https://github.com/qihuaha/test.git
git push -u origin master
