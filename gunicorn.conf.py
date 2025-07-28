# Configuração do Gunicorn para produção da Plataforma Curió
import os
import multiprocessing

# Configurações básicas
bind = f"0.0.0.0:{os.environ.get('PORT', 5000)}"
workers = int(os.environ.get("WEB_CONCURRENCY", "2"))
worker_class = "gthread"
threads = int(os.environ.get("WEB_THREADS", "2"))
timeout = 120
keepalive = 5

# Logging
accesslog = "-"
errorlog = "-"
loglevel = "info"

# Performance
preload_app = False  # deixe False a menos que tenha certeza que conexões não são criadas no import
max_requests = 1000
max_requests_jitter = 100
