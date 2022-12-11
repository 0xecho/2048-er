import os

if os.environ.get('ENVIRONMENT') == 'production':
    from .prod import *
elif os.environ.get('ENVIRONMENT') == 'test':
    from .test import *
else:
    from .dev import *