from flask import Flask, request, jsonify, send_from_directory
import os
import uuid
from datetime import datetime
from pathlib import Path
import logging
from logging.handlers import TimedRotatingFileHandler


app = Flask(__name__)

UPLOAD_FOLDER = r'explainer\uploads'
OUTPUT_FOLDER = r'explainer\outputs'
LOG_FOLDER = r'web_api\logs'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

log_handler = TimedRotatingFileHandler(os.path.join(LOG_FOLDER, 'web_api.log'), when="midnight", interval=1, backupCount=5)
log_handler.suffix = "%Y-%m-%d"
log_handler.setLevel(logging.INFO)
logger = logging.getLogger('WebAPILogger')
logger.addHandler(log_handler)
logger.setLevel(logging.INFO)


def generate_uid():
    return str(uuid.uuid4())

def get_current_time():
    return datetime.now().strftime("%Y-%m-%d[%H-%M-%S]")

def save_file(file, uid):
    curr_time = get_current_time()
    filename = f"{file.filename.rsplit('.', 1)[0]}_{curr_time}_{uid}.pptx"
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(file_path)
    return filename, curr_time

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        logger.error("No file part")
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        logger.error("No selected file")
        return jsonify({"error": "No selected file"}), 400
    
    uid = generate_uid()
    filename, timestamp = save_file(file, uid)
    logger.info(f"File uploaded: {filename.split('_')[0]} with uid: {uid}")
    return jsonify({"uid": uid, "filename": filename, "timestamp": timestamp})

@app.route('/status/<uid>', methods=['GET'])
def get_status(uid):
    upload_files = [f for f in os.listdir(UPLOAD_FOLDER) if uid in f]
    output_files = [f for f in os.listdir(OUTPUT_FOLDER) if uid in f]
    
    if not upload_files:
        logger.error(f"No file with the given uid: {uid}")
        return jsonify({"status": "No file with the given uid"}), 404
    
    if output_files:
        with open(os.path.join(OUTPUT_FOLDER, output_files[0]), 'r', encoding='utf-8') as f:
            summaries = f.read()
        logger.info(f"Summarization completed for {upload_files[0].split('_')[0]}") 
        return jsonify({
            "status": "completed",
            'filename': upload_files[0].rsplit('_', 2)[0],
            'timestamp': upload_files[0].rsplit('_', 2)[1],
            "summaries": summaries
        })
    else:
        logger.info(f"Summarization in progress for {upload_files[0].split('_')[0]}")
        return jsonify({
            "status": "in progress",
            'filename': upload_files[0].rsplit('_', 2)[0],
            'timestamp': upload_files[0].rsplit('_', 2)[1],
            'summaries': None
        })      
        
if __name__ == '__main__':
    print(f'Current working directory: {os.getcwd()}')
    app.run(debug=True)
