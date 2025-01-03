#!/bin/bash

# --- Configuration ---
PYTHON_SCRIPT="$HOME/proxy_toggle.py"  # Path to the Python script
LOG_FILE="$HOME/proxy_manager.log"    # Path to the log file
POLL_INTERVAL=10                     # Check interval in seconds
DATE_FORMAT="%Y-%m-%d %H:%M:%S"        # Log date format

# --- Functions ---
check_python_executable() {
    if [ ! -x "$PYTHON_SCRIPT" ]; then
        echo "$(date +"$DATE_FORMAT") - Error: Python script '$PYTHON_SCRIPT' is not executable." >> "$LOG_FILE"
        echo "Please run 'chmod +x $PYTHON_SCRIPT' to make it executable."
        exit 1
    fi
}

log_message() {
    echo "$(date +"$DATE_FORMAT") - $1" >> "$LOG_FILE"
}

run_proxy_script() {
    "$PYTHON_SCRIPT"
    if [ $? -ne 0 ]; then
        log_message "Error: Python script failed to execute."
        echo "Error: Python script failed to execute. See log file for more details."
        return 1
    fi
    return 0
}

handle_network_change() {
  while true; do
    run_proxy_script
    if [ $? -eq 0 ]; then
      log_message "Proxy settings checked."
    else
      log_message "Error: proxy settings check failed"
    fi
    sleep "$POLL_INTERVAL"
  done
}

# --- Main Script ---
# Create the log file if it doesn't exist
touch "$LOG_FILE"

# Check if script exist and make executable
check_python_executable

# Initial run when the script start
log_message "Proxy Manager script started."
run_proxy_script
if [ $? -eq 0 ]; then
  log_message "Initial proxy settings check done."
else
  log_message "Error: initial proxy check failed"
fi


# Run handler in the background
handle_network_change &

# Keep the main script running until interrupted
wait

log_message "Proxy Manager script stopped."
echo "Proxy Manager script stopped."
