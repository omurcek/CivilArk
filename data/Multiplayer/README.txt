CivilArk Multiplayer Guide

To enable multiplayer functionality for the 2D Python-based simulation game CivilArk, the Multiplayer folder includes the following essential files:

Core Files:

1. civilark_map.jpg: Used by the local server to properly process the game map.


2. open_source_server_for_developers.py: Python Flask-based server code for hosting a CivilArk server (you may need to configure your modem for external interaction).


3. open_source_server_run.bat: Script to automatically run the server on Windows.


4. open_source_server_run.sh: Script to automatically run the server on Linux.


5. target_server.txt: Stores the target server's address.


Setting Up Your Own Server:

1. Use a hosting service like PythonAnywhere (free option) or Replit (paid) to create a Python-based server.


2. Replace the main server code with the content of open_source_server_for_developers.py.


3. Integrate the civilark_map.jpg file into your server's working directory to set the map.


4. Run your server.

Connecting to a Server:

1. Edit the target_server.txt file to include the URL of the target server.
Important: The URL must not end with a trailing /.
Example:

https://civilark.pythonanywhere.com


2. Ensure the map file used by the target server matches the local map file located at:
data/Pictures/civilark_map.jpg


3. If you plan to use a custom player account, create or edit the player_account.txt file as follows:

USERNAME: <your_username>  
PASSWORD: <your_password>


4. Launch the CivilArk game, navigate to the Multiplayer section, and the game will automatically connect to the specified target server.



Enjoy multiplayer mode in CivilArk!

