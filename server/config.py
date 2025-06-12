from decouple import config

# HOST declarado en .env
HOST = config('HOST', default='0.0.0.0', cast=str)
# PORT declarado en .env
PORT = config('PORT', default=5000, cast=int)
# DEBUG declarado en .env
DEBUG = config('DEBUG', default=False, cast=bool)

