from decouple import config
import os

# Force production when running on Cloud Run, otherwise use ENV from environment or .env
if os.getenv('K_SERVICE'):
    ENV = "production"
else:
    ENV = config("ENV", default="development")

if ENV == "production":
    from .production import *
elif ENV == "staging":
    from .staging import *
else:
    from .development import *
