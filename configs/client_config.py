import os

base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))

LOGS_FOLDER = os.path.join(base_path, "client", "logs")
os.makedirs(LOGS_FOLDER, exist_ok=True)

LOG_FILE = os.path.join(LOGS_FOLDER, 'client.log')
UPLOAD_URL = 'http://127.0.0.1:5000/upload'
STATUS_URL = 'http://127.0.0.1:5000/status'



