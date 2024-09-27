import subprocess
import time

def main() -> None:
    """
    Executes a series of commands in separate terminal windows to run different services.

    The commands are:
    - run_web_api
    - run_explainer
    - run_client

    Each command is executed in a new terminal window with a delay of 1 second between each command.
    """
    # commands = [
    #     'start cmd /k run_web_api',
    #     'start cmd /k run_explainer',
    #     'start cmd /k run_client'
    # ]

    commands = [
        'start cmd /k python -m web_api.scripts.app',
        'start cmd /k python -m explainer.scripts.main',
        'start cmd /k python -m client.scripts.client'
    ]

    for command in commands:
        subprocess.Popen(command, shell=True)
        time.sleep(1) 

if __name__ == "__main__":
    main()
