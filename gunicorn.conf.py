import multiprocessing

# Maximum number of requests a worker will process before restarting (helps with memory leaks)
max_requests = 1000
max_requests_jitter = 50  # Random jitter to spread out restarts

# Log to stdout (you can change this to a specific file if needed)
log_file = "-"

# Bind the server to an IP and port (e.g., 0.0.0.0:5002)
bind = "0.0.0.0:5124"

# Preload the app before forking workers (shared memory for faster worker start-up)
preload_app = True

# Use the number of CPUs as the number of workers (workers per CPU core)
workers = multiprocessing.cpu_count()

# Alternatively, you could set workers like this (for more moderate load):
# workers = (multiprocessing.cpu_count() * 2) + 1

# Timeout for workers (in seconds), adjust based on your needs
timeout = 120

# Optionally, you can add log settings (access log, error log, etc.)
accesslog = "-"  # Log to stdout
errorlog = "-"   # Log to stderr
loglevel = "info"  # Set the logging level (info, debug, warning, error, critical)


