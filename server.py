from waitress import serve
import os
import api

PORT = os.getenv('PORT')
serve(api.app, port=(PORT if PORT else 8080))