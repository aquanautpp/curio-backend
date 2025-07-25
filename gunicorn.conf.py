# Configuração do Gunicorn para produção da Plataforma Curió
import os
import multiprocessing

# Configurações básicas
bind = f"0.0.0.0:{os.environ.get('PORT', 5000)}"
workers = min(4, (multiprocessing.cpu_count() * 2) + 1)
worker_class = "sync"
timeout = 120
keepalive = 5

# Logging
accesslog = "-"
errorlog = "-"
loglevel = "info"

# Performance
preload_app = True
max_requests = 1000
max_requests_jitter = 100

