import requests
import time
import os
from datetime import datetime
import logging
from logging.handlers import TimedRotatingFileHandler
import argparse

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
        
      
def input_path():
    while True:
        path = input("Enter the path of the file or 'r' to return menu: ")
        if path == "r": return
        if not os.path.exists(path):
            logger.error(f"An error occurred: File not found. Please enter a valid path.")
            continue
        try:
            uid = Status.upload_file(path)
            print(f"Uploaded file with uid: {uid}")
        
        except Exception as e:
                logger.error(f"An error occurred: {e}")
                print(f"An error occurred: {e}")
    
    
def check_status():
    path = input("Enter the UID of the file: ")
    try:
        status = Status.get_status(path)
        print(f"Status: {status.status}")
        if status.is_completed():
            print(f"Summaries: {status.summaries}")
    except Exception as e:
        print(f"An error occurred: {e}")
        logger.error(f"An error occurred: {e}")
    
        
        
def interactive_mode():
    while True:
        choice = input("Enter 1 to upload a file, 2 to check status, or 3 to exit: ")
        if choice != "1" and choice != "2" and choice != "3":
            print("Invalid choice. Please try again.")
            continue
        if choice == "3": exit(0)
        if choice == "1": input_path()
        if choice == "2": check_status()
        
        
            
def main():
    interactive_mode()
    
if __name__ == "__main__":
    main()