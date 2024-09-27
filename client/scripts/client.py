import requests
import time
import os
from datetime import datetime
import logging
from logging.handlers import TimedRotatingFileHandler
from configs import client_config as config



def setup_logger():
    log_handler = TimedRotatingFileHandler(config.LOG_FILE, when="midnight", interval=1, backupCount=5)
    log_handler.suffix = "%Y-%m-%d"
    log_handler.setLevel(logging.INFO)
    logger = logging.getLogger('ClientLogger')
    logger.addHandler(log_handler)
    logger.setLevel(logging.INFO)
    return logger

logger = setup_logger()

class Status:
    def __init__(self, status: str, filename: str, timestamp: str, summaries: dict):
        """
        Initializes a Status object.
        
        Parameters:
        - status (str): The status of the processing.
        - filename (str): The name of the file being processed.
        - timestamp (str): The timestamp when the status was updated.
        - summaries (dict): The summaries generated from the presentation.
        """
        self.status = status
        self.filename = filename
        self.timestamp = timestamp
        self.summaries = summaries
  
        
    def is_completed(self) -> bool:
        """
        Checks if the processing status is completed.
        
        Returns:
        - bool: True if the status is 'completed', otherwise False.
        """
        return self.status == "completed"
  
    
    @staticmethod
    def upload_file(file_path: str) -> str:
        """
        Uploads a file to the server.
        
        Parameters:
        - file_path (str): The path to the file to be uploaded.
        
        Returns:
        - str: The UID of the uploaded file.
        
        Raises:
        - Exception: If there is an error uploading the file.
        """
        url = config.UPLOAD_URL
        try:
            with open(file_path, 'rb') as file:
                files = {'file': file}
                response = requests.post(url, files=files)
                response.raise_for_status()
                uid = response.json()['uid']
                logger.info(f"File uploaded successfully. UID: {uid}")
                return uid
        except Exception as e:
            logger.error(f"Error uploading file: {e}")
            raise e
   
        
    @staticmethod
    def get_status(uid: str) -> 'Status':
        """
        Retrieves the processing status of a file from the server.
        
        Parameters:
        - uid (str): The UID of the file.
        
        Returns:
        - Status: A Status object with the current status, filename, timestamp, and summaries.
        
        Raises:
        - Exception: If there is an error retrieving the status.
        """
        url = f'{config.STATUS_URL}/{uid}'
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            logger.info(f"Status for UID {uid}: {data['status']}")
            return Status(data['status'], data['filename'], data['timestamp'], data['summaries'])
        except Exception as e:
            logger.error(f"Error getting status: {e}")
            raise e

def input_path() -> None:
    """
    Prompts the user to enter the path of the file to be uploaded and uploads it.
    """
    while True:
        path = input("Enter the path file:  ")
        if path == "r": return
        if not os.path.exists(path):
            logger.error("An error occurred: File not found. Please enter a valid path.")
            continue
        try:
            uid = Status.upload_file(path)
            print(f"Uploaded file with uid: {uid}")
            check_status()
            return
        except Exception as e:
            logger.error(f"An error occurred: {e}")
            print(f"An error occurred: {e}")

def check_status() -> None:
    """
    Prompts the user to enter the UID of the file and retrieves its processing status.
    """
    uid = input("Enter the UID of the file: ")
    try:
        status = Status.get_status(uid)
        print(f"Status: {status.status}")
        if status.is_completed():
            print(f"Summaries: {status.summaries}")
    except Exception as e:
        print(f"An error occurred: {e}")
        logger.error(f"An error occurred: {e}")

def print_intro():
    intro_message = """
    \033[1;34m
    ***********************************************
    *                                             *
    *                    CLIENT                    *
    *                                             *
    ***********************************************
    * This is the client interface for the        *
    * explainer project.                          *
    *                                             *
    * Usage:                                      *
    *   - Use this interface to upload files and  *
    *     check their status.                     *
    *                                             *
    ***********************************************
    \033[0m
    """
    print(intro_message)

def interactive_mode() -> None:
    """
    Provides an interactive mode for the user to upload files or check their status.
    """
    print_intro()
    while True:
        choice = input("\nPlease choose a number:\n"
                       "1. Upload\n"
                       "2. Check status\n"
                       "3. Exit\n"
                       "Enter your choice: ")

        if choice not in ["1", "2", "3"]:
            print("Invalid choice. Please try again.")
            continue
        if choice == "3": exit(0)
        if choice == "1": input_path()
        if choice == "2": check_status()

def main() -> None:
    """
    Main function to start the interactive mode.
    """
    interactive_mode()

if __name__ == "__main__":
    main()
