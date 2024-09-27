import os

base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))

UPLOADS_FOLDER = os.path.join(base_path, "explainer", "uploads")
OUTPUTS_FOLDER = os.path.join(base_path, "explainer", "outputs")
LOGS_FOLDER = os.path.join(base_path, "explainer", "logs")

os.makedirs(UPLOADS_FOLDER, exist_ok=True)
os.makedirs(OUTPUTS_FOLDER, exist_ok=True)
os.makedirs(LOGS_FOLDER, exist_ok=True)

LOG_FILE = os.path.join(LOGS_FOLDER, 'explainer.log')
