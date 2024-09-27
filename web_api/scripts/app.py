from flask import Flask, request, jsonify, send_from_directory
import os
import uuid
from datetime import datetime
import logging
from logging.handlers import TimedRotatingFileHandler
from configs import web_api_config as config

app = Flask(__name__)

def setup_logger():
    log_handler = TimedRotatingFileHandler(config.LOG_FILE, when="midnight", interval=1, backupCount=5)
    log_handler.suffix = "%Y-%m-%d"
    log_handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    log_handler.setFormatter(formatter)

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(formatter)

    logger = logging.getLogger('WebAPILogger')
    logger.setLevel(logging.INFO)
    logger.addHandler(log_handler)
    logger.addHandler(stream_handler)
    return logger

logger = setup_logger()

def generate_uid() -> str:
    return str(uuid.uuid4())

def get_current_time() -> str:
    return datetime.now().strftime("%Y-%m-%d[%H-%M-%S]")

def save_file(file, uid: str) -> tuple[str, str]:
    curr_time = get_current_time()
    filename = f"{file.filename.rsplit('.', 1)[0]}_{curr_time}_{uid}.pptx"
    file_path = os.path.join(config.UPLOAD_FOLDER, filename)
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
def get_status(uid: str):
    upload_files = [f for f in os.listdir(config.UPLOAD_FOLDER) if uid in f]
    output_files = [f for f in os.listdir(config.OUTPUT_FOLDER) if uid in f]
    
    if not upload_files:
        logger.error(f"No file with the given uid: {uid}")
        return jsonify({"status": "No file with the given uid"}), 404
    
    if output_files:
        with open(os.path.join(config.OUTPUT_FOLDER, output_files[0]), 'r', encoding='utf-8') as f:
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

def print_intro():
    intro_message = """
    \033[1;35m
    ***********************************************
    *                                             *
    *                   WEB API                   *
    *                                             *
    ***********************************************
    * This is the main web API for the explainer  *
    * project.                                    *
    *                                             *
    * Usage:                                      *
    *   - Run this script to start the web API.   *
    *                                             *
    ***********************************************
    \033[0m
    """
    print(intro_message)

def main() -> None:
    print_intro()
    app.run(debug=True)

if __name__ == '__main__':
    main()
