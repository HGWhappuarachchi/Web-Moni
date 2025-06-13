# NetMoni - Network Latency Monitor & Alerter

  

A modern, cross-platform desktop application for visually monitoring network device latency with pop-out widgets, a detailed dashboard, and automated email alerts.

\<br\>

## Table of Contents

  - [About The Project](https://www.google.com/search?q=%23about-the-project)
  - [Key Features](https://www.google.com/search?q=%23key-features)
  - [Technology Stack](https://www.google.com/search?q=%23technology-stack)
  - [Getting Started](https://www.google.com/search?q=%23getting-started)
      - [Prerequisites](https://www.google.com/search?q=%23prerequisites)
      - [Installation & Setup](https://www.google.com/search?q=%23installation--setup)
  - [Usage](https://www.google.com/search?q=%23usage)
  - [Compiling for Distribution](https://www.google.com/search?q=%23compiling-for-distribution)

## About The Project

NetMoni provides a simple yet powerful solution for IT professionals and tech enthusiasts who need to keep a constant eye on the health of multiple network devices. It replaces traditional command-line pinging with an intuitive graphical dashboard, featuring analog-style gauges that provide immediate, at-a-glance feedback on the latency of your servers, routers, and other critical IPs.

With features like individual logging, pop-out desktop widgets, and automated email alerts for outages, NetMoni transforms reactive troubleshooting into proactive monitoring.

## Key Features

  * **Live Latency Monitoring:** Track multiple IP addresses simultaneously in real-time using the system's native ping command.
  * **Visual Analog Dashboard:** An intuitive main dashboard displays each monitored device as an analog gauge, showing latency in milliseconds and providing instant visual feedback on network health.
  * **Pop-out Desktop Widgets:** Any gauge can be "popped out" into its own standalone desktop window for persistent monitoring.
  * **Advanced Widget Customization:**
      * **Persistent Positioning:** Widgets remember their last location on your desktop, saved directly to the database.
      * **Draggable Grab Bar:** A dedicated bar at the top of each widget allows for easy and predictable repositioning.
      * **Hover Opacity:** Widgets are semi-transparent by default and become fully opaque when you mouse over them, keeping your desktop clean.
  * **Right-Click Widget Menu:** Each desktop widget is fully controllable via a right-click context menu offering:
      * **Resize:** Instantly change the widget's size between Small, Medium, and Large presets.
      * **Keep on Top:** Toggle whether the widget should always stay on top of other windows.
      * **Close:** Close the widget and save its state.
  * **Automated Email Alerts:** Configure the app to send email notifications via an Office 365 account to a list of recipients after a device experiences a set number of consecutive timeouts.
  * **Per-IP Logging & In-App Viewer:** Every monitored device has its own dedicated log file stored in a `logs` folder. You can view the detailed logs for any device directly from the main dashboard.
  * **Full GUI for Configuration:** All administrative tasks—managing IPs, alert recipients, and the sender email account—are handled through a simple and clear settings panel.

## Technology Stack

This project is built with Python and leverages the following key libraries:

  * [**CustomTkinter**](https://github.com/TomSchimansky/CustomTkinter): For the modern graphical user interface.
  * **SQLite3:** For all persistent data storage (part of the standard Python library).
  * **Pillow:** For image handling with the system tray icon.
  * **pystray:** For creating and managing the background system tray icon.

## Getting Started

To get a local copy up and running, follow these steps.

### Prerequisites

  * Python 3.8 or newer.
  * `pip` for installing packages.

### Installation & Setup

1.  **Clone the repository (or download the files):**
    ```sh
    git clone https://github.com/your_username/NetMoni.git
    cd NetMoni
    ```
2.  **Create a Virtual Environment (Recommended):**
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```
3.  **Install Dependencies:**
    ```sh
    pip install customtkinter Pillow pystray
    ```
4.  **Initialize the Database:**
    Before the first run, execute the database script to create the `monitor_app.db` file.
    ```sh
    python database.py
    ```
5.  **Run the Application:**
    Launch the main application script. The app will start minimized in the system tray.
    ```sh
    python main_app.py
    ```

## Usage

1.  **Launch the App:** After running `main_app.py`, find the NetMoni icon in your computer's system tray (near the clock).
2.  **Open the Dashboard:** Right-click the tray icon and select "Show Dashboard".
3.  **Configure:** In the dashboard window, click "Settings" on the sidebar to:
      * Add IPs to monitor.
      * Add user emails for alerts.
      * Set up your Office 365 email credentials for sending alerts.
4.  **Monitor:** Use the dashboard to view all gauges or click the "Widget" button on any gauge to pop it out onto your desktop for persistent viewing.

## Compiling for Distribution

You can compile the project into a single `NetMoni.exe` file for easy sharing and execution on other Windows machines.

1.  **Install PyInstaller:**
    ```sh
    pip install pyinstaller
    ```
2.  **Prepare Icons:** Make sure you have two icon files in your project directory:
      * `icon.ico`: For the `.exe` file itself.
      * `icon.png`: For the system tray icon (Pillow works best with PNG).
3.  **Run the Build Command:**
    Open a terminal in your project directory and execute the following command:
    ```sh
    pyinstaller --onefile --windowed --name NetMoni --icon=icon.ico --add-data "icon.png;." main_app.py
    ```
4.  **Find Your Application:** The final `NetMoni.exe` will be located in the `dist` folder.
