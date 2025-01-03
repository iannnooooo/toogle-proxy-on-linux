# Proxy Manager

## Overview
`proxy_manager.sh` is a Bash script designed to dynamically manage proxy settings based on network changes. It integrates seamlessly with a Python script, `proxy_toggle.py`, for advanced proxy configuration.

## How to Use

### 1. Save the Script
Save the Bash script as `proxy_manager.sh`.

### 2. Make it Executable
Run the following command to make the script executable:
```bash
chmod +x proxy_manager.sh
```

### 3. Run the Script
Execute the script using:
```bash
./proxy_manager.sh
```

### 4. Stop the Script
To stop the script, use:
```bash
Ctrl+C
```

---

## Integration with Python Script

### Prerequisites
1. Save your Python script as `proxy_toggle.py` in the directory specified in `proxy_manager.sh`.
2. Ensure the Python script is executable:
   ```bash
   chmod +x proxy_toggle.py
   ```

---

## Enhancements and Considerations

### Logging
- Add logging to `proxy_manager.sh` to track when the proxy is enabled/disabled and assist with troubleshooting.

### Error Handling
- Improve the script by adding robust error handling mechanisms.

### Background Service
For better reliability, you can integrate `proxy_manager.sh` with `systemd` to run it as a background service that starts at boot.

### Polling Interval
- Adjust the polling interval in the `handle_network_change` function by modifying the `sleep 10` command.
  - A smaller interval ensures more responsive proxy configuration but consumes more system resources.

---

## Steps to Create a systemd Service

### 1. Create a Service File
Create a file at `/etc/systemd/system/proxy_manager.service` with the following content:
```ini
[Unit]
Description=Proxy Manager Service
After=network.target

[Service]
Type=simple
User=<YOUR_USERNAME>  # Replace this with your username
WorkingDirectory=<YOUR_DIRECTORY>  # Replace this with the directory of proxy_manager.sh
ExecStart=/bin/bash <YOUR_DIRECTORY>/proxy_manager.sh  # Replace with the full path to proxy_manager.sh
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

### 2. Update the Service File
Replace:
- `<YOUR_USERNAME>` with your username.
- `<YOUR_DIRECTORY>` with the full path to the `proxy_manager.sh` script.

### 3. Enable and Start the Service
Enable and start the service with the following commands:
```bash
sudo systemctl enable proxy_manager.service
sudo systemctl start proxy_manager.service
```

### 4. Check the Service Status
To check the status of the service, run:
```bash
sudo systemctl status proxy_manager.service
```

---

## License
Use this script with caution and modify it to suit your needs. Ensure proper testing before deploying it in production.

---

## Disclaimer
This script is provided as-is without warranty of any kind. The user assumes all responsibility for any issues arising from its use.

