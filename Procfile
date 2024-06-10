web: gunicorn ecommerce_backend.wsgi:application --log-file -
asgi: uvicorn ecommerce_backend.asgi:application --host 0.0.0.0 --port $PORT
