# Gunicorn configuration for Shakespeare Census

import os

BASE_DIR = os.environ.get("H", "/code")

errorlog = "-"
bind = "0.0.0.0:8000"
log_level = "INFO"
workers = 1
worker_tmp_dir = "/dev/shm"

keepalive = 32

pythonpath = BASE_DIR
chdir = BASE_DIR
