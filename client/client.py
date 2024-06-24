import requests
import time
from datetime import datetime

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
        with open(file_path, 'rb') as file:
            files = {'file': file}
            response = requests.post(url, files=files)
            response.raise_for_status() # Raise an exception for 4xx/5xx status codes
            return response.json()['uid']
        
    @staticmethod
    def get_status(uid):
        url = f'http://127.0.0.1:5000/status/{uid}'
        response = requests.get(url) # GET request
        response.raise_for_status() # Raise an exception for 4xx/5xx status codes
        data = response.json()
        return Status(data['status'], data['filename'], data['timestamp'], data['summaries'])
        
if __name__ == "__main__":
    while True:
        path = input("Enter the path of the file: ")
        if path.lower() == "exit":
            exit(0)
        uid = Status.upload_file(path)
        print(f"Uploaded file with uid: {uid}")
        print("Waiting sumerized to completed", end="", flush=True)
                
        status = Status.get_status(uid)
        counter = 1
        while not status.is_completed():
            if counter % 4 == 0:
                print()
            else:
                print(".", end="", flush=True)
            counter += 1
            time.sleep(1)
            status = Status.get_status(uid)
        
        print(f"\nSummaries: {status.summaries}")
