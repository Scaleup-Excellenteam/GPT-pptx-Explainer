import os

base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))

UPLOAD_FOLDER = os.path.join(base_path, "explainer", "uploads")
OUTPUT_FOLDER = os.path.join(base_path, "explainer", "outputs")
LOG_FOLDER = os.path.join(base_path, "web_api", "logs")

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)
os.makedirs(LOG_FOLDER, exist_ok=True)

LOG_FILE = os.path.join(LOG_FOLDER, 'web_api.log')
