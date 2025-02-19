# CosmicAI Backend

This is a Flask application that is configured to run with Gunicorn for production environments. This README provides instructions on how to set up and run the app using Gunicorn, including configuration settings for optimal performance.

## Requirements

Ensure you have the following installed:

- Python 3.x
- Flask
- Gunicorn
- Other dependencies (e.g., `flask_sqlalchemy`, `flask_jwt_extended`, etc.)

You can install the dependencies using:

```bash
pip install -r requirements.txt
```

### 1. Setup `.env` File

Make sure you have a `.env` file in your project root to set up any necessary environment variables such as `JWT_SECRET`, `SQLALCHEMY_DATABASE_URI`, etc. If you're unsure of the variables, they should be defined in your `create_app()` function.

---

## Gunicorn Setup

### 2. Gunicorn Configuration

We use a `gunicorn.conf.py` file to define Gunicorn configuration settings. Here's an overview of the main settings:

- **max_requests**: Limits the number of requests a worker can handle before it is restarted.
- **max_requests_jitter**: Adds a small random jitter to worker restarts, spreading them out over time.
- **log_file**: Specifies where the logs are saved. In this case, logs are output to stdout (`"-"`).
- **bind**: Defines the address and port that Gunicorn binds to (e.g., `0.0.0.0:5002`).
- **preload_app**: Preloads the app into memory for faster worker start-up.
- **workers**: Configures the number of workers to spawn (based on available CPU cores).
- **timeout**: Specifies how long Gunicorn will wait for a worker to respond before timing out.

---

## Running Gunicorn with Configuration File

Once the setup is complete, you can run Gunicorn with your custom configuration by executing the following command:

```bash
gunicorn -c gunicorn.conf.py 'app:create_app()'
```

### Explanation of the Command:

- **`gunicorn`**: This is the command to run Gunicorn.
- **`-c gunicorn.conf.py`**: This tells Gunicorn to load the configuration settings from the `gunicorn.conf.py` file.
- **`'app:create_app()'`**: This specifies the application factory function `create_app()` inside the `app.py` file to create and run the Flask app.

---

## Troubleshooting

### Common Errors:

1. **Error: `Failed to find attribute 'app' in 'app'`**:

   - This usually happens when the `create_app()` function is not correctly referenced in Gunicorn. Ensure you're using the command: `gunicorn -c gunicorn.conf.py 'app:create_app()'`.

2. **Missing Environment Variables**:

   - If the `.env` file is missing or misconfigured, the app may fail to load. Make sure all required variables (such as `SQLALCHEMY_DATABASE_URI` and `JWT_SECRET`) are set in `.env`.

3. **Memory Issues**:
   - If your application is consuming too much memory or is slow, you can tweak the `workers` and `timeout` settings in `gunicorn.conf.py` for better performance.

---

## Api Docs

Api docs for app is here in route:

```bash
/api/docs/
```

---

## Created By

**Sagar Patel**  
GitHub: [@sagarpatel0412](https://github.com/sagarpatel0412)

---
