# Gunicorn configuration file
import os

# Server socket
bind = "0.0.0.0:" + os.environ.get("PORT", "10000")
backlog = 2048

# Worker processes
workers = 1
worker_class = "sync"
worker_connections = 200
# Increase timeout to 120 seconds to prevent worker timeouts on slow requests
timeout = 120
keepalive = 2

# Restart workers after this many requests, to help prevent memory leaks
max_requests = 1000
max_requests_jitter = 50

# Logging
accesslog = "-"
errorlog = "-"
loglevel = "info"

# Process naming
proc_name = "budge-it-app"

# Server mechanics
daemon = False
pidfile = None
umask = 0
user = None
group = None
tmp_upload_dir = None

# SSL (not needed for Render)
keyfile = None
certfile = None

# Preload app for better performance
preload_app = True

# Worker timeout
graceful_timeout = 30

# Maximum requests per worker
max_requests = 1000
max_requests_jitter = 50

# Worker restart after this many requests
worker_tmp_dir = None

# Worker class
worker_class = "sync"

# Worker connections
worker_connections = 200

# Timeout
timeout = 30

# Keep alive
keepalive = 2

# Limit request line size
limit_request_line = 4094

# Limit request fields
limit_request_fields = 100

# Limit request field size
limit_request_field_size = 8190