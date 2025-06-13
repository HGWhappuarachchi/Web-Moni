NetMoni - Network Latency Monitor
A modern desktop application for monitoring network device latency with a visual dashboard, pop-out widgets, and automated email alerts.

(Feel free to replace the image link above with a screenshot of your own application)

About The Project
NetMoni was created to provide a simple yet powerful solution for IT professionals and tech enthusiasts who need to keep a constant eye on the health of multiple network devices. Instead of using command-line tools, NetMoni offers an intuitive graphical dashboard with analog-style gauges that provide immediate, at-a-glance feedback on the latency of your servers, routers, and other critical IPs.

With features like individual logging, pop-out widgets, and automated email alerts, NetMoni transforms reactive troubleshooting into proactive monitoring.

Features
Live Latency Monitoring: Track multiple IP addresses simultaneously in real-time.
Visual Analog Gauges: An intuitive dashboard displays each device's latency (in ms) on a dedicated gauge with color-coded health indicators (Green/Yellow/Red).
Pop-out Desktop Widgets: Any gauge can be popped out into its own standalone window. These widgets feature:
Persistent Positioning: Widgets remember their last location on your desktop.
Draggable Grab Bar: A dedicated bar at the top of each widget allows for easy repositioning.
Hover Opacity: Widgets are semi-transparent and become fully opaque when you mouse over them, keeping your desktop clean.
Right-Click Widget Menu: Each desktop widget is fully controllable via a right-click menu:
Resize: Instantly change the widget's size between Small, Medium, and Large presets.
Keep on Top: Toggle whether the widget should always stay on top of other windows.
Close: Close the widget and save its last known position and settings.
Automated Email Alerts: Configure the app to send email notifications to a list of recipients via Office 365 when a device experiences 5 (or more) consecutive timeouts.
Per-IP Logging: Every monitored device has its own dedicated log file stored in a logs folder, tracking every success, failure, and recovery event with a timestamp.
In-App Log Viewer: View the detailed logs for any device directly from the main dashboard without needing to open text files manually.
Full GUI Configuration: No code changes are needed after setup. All administrative tasks are handled through the UI:
Manage IPs and their descriptions.
Manage the list of email alert recipients.
Securely configure the sender email account.
Getting Started
To get a local copy up and running, follow these simple steps.

Prerequisites
You need to have Python installed on your system. Then, install the required library using pip:

Bash

pip install customtkinter
Running the Application
The project consists of the following essential files:

main_app.py (The main application)
database.py (Handles database creation and interaction)
ctk_meter.py (The custom gauge widget)
pinger.py (The ping logic)
logger_setup.py (Handles individual log files)
emailer.py (Handles sending alert emails)
<!-- end list -->

Make sure all the .py files are in the same folder.
Run the database.py script once to create and initialize the database file (monitor_app.db):
Bash

python database.py
Run the main application:
Bash

python main_app.py
Usage
First-Time Setup:

Launch the application.
Click on "Settings" in the left sidebar.
Use "Manage IPs to Monitor" to add the IP addresses you want to track.
Use "Manage Alert Recipients" to add the email addresses that should receive alerts.
Use "Configure Email Account" to enter your Office 365 sender email and an App Password for sending alerts.
Monitoring:

Click "Dashboard" to view the live status of all your configured IPs.
Using Widgets:

Click the "Widget" button below any gauge to pop it out.
Click and drag the gray bar at the top of the widget to move it.
Right-click the widget to access options for resizing or pinning it on top.
Compiling into an .exe (Optional)
You can compile the entire project into a single NetMoni.exe file for easy distribution.

Install the PyInstaller library:
Bash

pip install pyinstaller
Place an icon file named icon.ico in your project folder.
Run the following command in your terminal from the project directory:
Bash

pyinstaller --onefile --windowed --name NetMoni --icon=icon.ico main_app.py
The final NetMoni.exe will be located in the dist folder.
