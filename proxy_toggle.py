import socket
import os
import subprocess
import sys
import platform

PROXY_SERVER = "http://your_proxy_server:port"  # Replace with your proxy details
NO_PROXY_LIST = "localhost,127.0.0.1" #Add other necessary no_proxy domains

def is_private_ip(ip_address):
    try:
        # Convert IP to integer
        ip_int = int(socket.inet_aton(ip_address).hex(), 16)
        # 172.16.0.0/12 range
        return 2886729728 <= ip_int <= 2887772159
    except OSError: # catches the exception for a invalid ip like 127.0.0.1, ::1 or anything other than ipv4
        return False

def set_proxy_variables(enable=True):
    if enable:
        os.environ['HTTP_PROXY'] = PROXY_SERVER
        os.environ['HTTPS_PROXY'] = PROXY_SERVER
        os.environ['NO_PROXY'] = NO_PROXY_LIST
        print("Proxy Enabled")
    else:
        os.environ.pop('HTTP_PROXY', None)
        os.environ.pop('HTTPS_PROXY', None)
        os.environ.pop('NO_PROXY', None)
        print("Proxy Disabled")

    # This ensures that the env vars are updated in shell by using subprocess
    if platform.system() == 'Windows':
        subprocess.run('SETX HTTP_PROXY {}'.format(os.environ.get('HTTP_PROXY',"")),shell=True)
        subprocess.run('SETX HTTPS_PROXY {}'.format(os.environ.get('HTTPS_PROXY',"")),shell=True)
        subprocess.run('SETX NO_PROXY {}'.format(os.environ.get('NO_PROXY',"")),shell=True)
    else:
         subprocess.run('export HTTP_PROXY={}'.format(os.environ.get('HTTP_PROXY',"")),shell=True)
         subprocess.run('export HTTPS_PROXY={}'.format(os.environ.get('HTTPS_PROXY',"")),shell=True)
         subprocess.run('export NO_PROXY={}'.format(os.environ.get('NO_PROXY',"")),shell=True)


def get_current_ip():
    try:
        # Attempt to get the IP by connecting to google public dns
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception as e:
        print(f"Error getting IP: {e}")
        return None

def main():
    current_ip = get_current_ip()

    if current_ip:
        if is_private_ip(current_ip):
            set_proxy_variables(enable=True)
        else:
            set_proxy_variables(enable=False)
    else:
        print("Could not determine IP, exiting...")
        sys.exit(1)

if __name__ == "__main__":
    main()
