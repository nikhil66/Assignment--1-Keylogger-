This is a basic keylogger that also captures screenshots and clipboard info and uploads the data to a server on github.

We start out by defining some functions but before that we create two empty files on the victims device to hold our data temporarily until it is uploaded.

update_github_file is the fucntion used to upload the data to the server and also encoding the data in b64 because github requires you to do so.

create_github_file is the function used to create files, we need this because each screenshot is a different file.

monitor_clipboard logs the clipboard contents every 3 seconds to clip.txt
*only if it is not the same as the previous contents

on_press key is the main fucntion that logs all the keys including special keys like Shift and Ctrl to log.txt

capture_screenshot is a simple function that takes a screenshot of the victims screen.

We use threading to keep the functions running all the time

The last part of the code gets ready to upload all the contents of clip.txt and log.txt every 5 seconds along with creating a new file for the screenshot and uploading the screenshot. All this is uploaded along with the time.
