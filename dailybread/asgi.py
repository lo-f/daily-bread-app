"""
ASGI config for dailybread project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os
from dotenv import load_dotenv

load_dotenv()

API_ID = os.getenv("API_ID")
API_KEY = os.getenv("API_KEY")

from django.core.asgi import get_asgi_application


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dailybread.settings')

application = get_asgi_application()
