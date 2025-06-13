
import subprocess
import re
import os

def check_latency(target_ip):
    """
    Pings the target IP and returns the latency in ms.
    Returns None if the ping fails.
    """
    try:
        # For Windows: -n 1 (1 packet), -w 2000 (2-second timeout)
        command = ["ping", "-n", "1", "-w", "2000", target_ip]
        if os.name != "nt": # For Linux/macOS
            command = ["ping", "-c", "1", "-W", "2", target_ip]

        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            encoding='latin-1',
            creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
        )

        if result.returncode == 0:
            for line in result.stdout.splitlines():
                if "time=" in line or "time<" in line:
                    match = re.search(r"time[=<]([\d.]+)", line)
                    if match:
                        return float(match.group(1))
        return None
    except Exception:
        return None