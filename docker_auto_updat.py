import requests
import time
import os,sys
from dotenv import load_dotenv
import subprocess
sys.tracebacklimit = -1

load_dotenv()
username = os.getenv("DOCKERHUB_USERNAME")
access_token = os.getenv("DOCKERHUB_ACCESS_TOKEN")
repository_name = "test"
api_url = f"https://hub.docker.com/v2/repositories/{username}/{repository_name}"


def updat_it(last_push):

    # Define the make up command as a list of strings
    make_up_command = ["make", "update"]
        # Use subprocess.run() to execute the make up command
    result = subprocess.run(make_up_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode == 0:
        print("Make up completed successfully")
        print(f"Stored Last Push")
        with open(".last_update", "w") as file:
            file.write(last_push)
    else:
        print("Make up failed with the following output:")
        print(result.stdout)
        print(result.stderr)



# Function to get the last push timestamp for the repository
def get_last_push_timestamp():
    try:
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()
        data = response.json()
        last_push = data.get("last_updated")
        return last_push
    except Exception as e:
        print(f"Error: {e}")
        return None

# Function to check if there is a new push
def check_for_new_push():
    last_push = get_last_push_timestamp()
    
    try:
        with open(".last_update", "r") as file:
            stored_last_push = file.read().strip()

        if last_push != stored_last_push:
            print ("old",stored_last_push,"\n new:",last_push)
            updat_it(last_push)         

        else:
            print("Last Push and Stored Last Push are the same.")
    except FileNotFoundError:

        updat_it(last_push)         


if __name__ == "__main__":
    check_for_new_push()


