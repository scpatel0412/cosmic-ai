from app import create_app
import os

app = create_app()

if os.environ.get("FLASK_ENV") == "development":
    if __name__ == '__main__':
        port = int(os.environ.get("PORT", 5000))
        app.run(port=port, debug=True)
elif os.environ.get("FLASK_ENV") == "production":
    if __name__ == '__main__':
        port = int(os.environ.get("PORT", 5000))
        app.run(host="0.0.0.0", port=port, debug=True)
else:
    if __name__ == '__main__':
        port = int(os.environ.get("PORT", 5000))
        app.run(port=port, debug=True)
