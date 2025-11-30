from decouple import config

ENV = config("ENV", "development")

if ENV == "production":
    from .production import *
elif ENV == "staging":
    from .staging import *
else:
    from .development import *
