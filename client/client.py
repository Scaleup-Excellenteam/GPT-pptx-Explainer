import requests
import time
import os
from datetime import datetime
import logging
from logging.handlers import TimedRotatingFileHandler

LOGS_FOLDER = r'logs'
os.makedirs(LOGS_FOLDER, exist_ok=True)

log_handler = TimedRotatingFileHandler(os.path.join(LOGS_FOLDER, 'client.log'), when="midnight", interval=1, backupCount=5) # Keep 5 backup files
log_handler.suffix = "%Y-%m-%d"
log_handler.setLevel(logging.INFO)
logger = logging.getLogger('ClientLogger')
logger.addHandler(log_handler)
logger.setLevel(logging.INFO)

class Status:
    def __init__(self, status, filename, timestamp, summaries):
        self.status = status
        self.filename = filename
        self.timestamp = timestamp
        self.summaries = summaries
        
    def is_completed(self):
        return self.status == "completed"
    
    @staticmethod
    def upload_file(file_path):
        url = 'http://127.0.0.1:5000/upload'
        try:
            with open(file_path, 'rb') as file:
                files = {'file': file}
                response = requests.post(url, files=files)
                response.raise_for_status()  # Raise an exception for 4xx/5xx status codes
                uid = response.json()['uid']
                logger.info(f"File uploaded successfully. UID: {uid}")
                return uid
        except Exception as e:
            logger.error(f"Error uploading file: {e}")
            raise e
        
    @staticmethod
    def get_status(uid):
        url = f'http://127.0.0.1:5000/status/{uid}'
        try:
            response = requests.get(url)  # GET request
            response.raise_for_status()  # Raise an exception for 4xx/5xx status codes
            data = response.json()
            logger.info(f"Status for UID {uid}: {data['status']}")
            return Status(data['status'], data['filename'], data['timestamp'], data['summaries'])
        except Exception as e:
            logger.error(f"Error getting status: {e}")
            raise e
        
if __name__ == "__main__":
    while True:
        path = input("Enter the path of the file: ")
        if path.lower() == "exit":
            exit(0)
        try:
            uid = Status.upload_file(path)
            print(f"Uploaded file with uid: {uid}")
            print("Waiting for summarization to complete", end="", flush=True)
                    
            status = Status.get_status(uid)
            counter = 1
            while not status.is_completed():
                if counter % 4 == 0:
                    print()
                else:
                    print(".", end="", flush=True)
                counter += 1
                time.sleep(0.5)
                status = Status.get_status(uid)
            
            print(f"\nSummaries: {status.summaries}")
            logger.info(f"Summarization completed for UID: {uid}")
        except Exception as e:
            logger.error(f"An error occurred: {e}")
            print(f"An error occurred: {e}")
