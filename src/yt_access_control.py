import os
import platform
from termcolor import colored

# Detect the operating system
OS_NAME = platform.system()

# Determine the hosts file path based on the OS
if OS_NAME == "Windows":
    HOSTS_FILE = r"C:\Windows\System32\drivers\etc\hosts"
else:  # macOS & Linux
    HOSTS_FILE = "/etc/hosts"

YOUTUBE_DOMAINS = ["youtube.com", "www.youtube.com"]
REDIRECT_IP = "127.0.0.1"

def is_admin():
    """Check if script is running with administrator (Windows) or root (macOS/Linux) privileges."""
    if OS_NAME == "Windows":
        return os.system("net session >nul 2>&1") == 0
    else:  # macOS/Linux
        return os.geteuid() == 0

def is_youtube_blocked():
    """Check if YouTube is already blocked in the hosts file."""
    with open(HOSTS_FILE, "r") as file:
        content = file.read()
        return any(f"{REDIRECT_IP} {domain}" in content for domain in YOUTUBE_DOMAINS)

def unblock_youtube():
    """Unblock YouTube by removing entries from the hosts file."""
    if not is_youtube_blocked():
        print(colored("✅ YouTube is already unblocked.", "green"))
        return
    
    with open(HOSTS_FILE, "r") as file:
        lines = file.readlines()
    
    with open(HOSTS_FILE, "w") as file:
        for line in lines:
            if not any(f"{REDIRECT_IP} {domain}" in line for domain in YOUTUBE_DOMAINS):
                file.write(line)
    print(colored("✅ YouTube has been unblocked.", "green"))

def block_youtube():
    """Block YouTube by adding entries to the hosts file."""
    if is_youtube_blocked():
        print(colored("✅ YouTube is already blocked.", "green"))
        return
    
    with open(HOSTS_FILE, "r+") as file:
        content = file.readlines()
        file.seek(0)
        for line in content:
            if not any(domain in line for domain in YOUTUBE_DOMAINS):
                file.write(line)
        for domain in YOUTUBE_DOMAINS:
            file.write(f"{REDIRECT_IP} {domain}\n")
        file.truncate()
    print(colored("✅ YouTube has been blocked.", "green"))

def flush_dns():
    """Flush DNS cache to apply changes immediately."""
    if OS_NAME == "Windows":
        os.system("ipconfig /flushdns")
    elif OS_NAME == "Darwin":  # macOS
        os.system("sudo dscacheutil -flushcache")
    elif OS_NAME == "Linux":
        os.system("sudo systemctl restart nscd")  # For systems using nscd
    print(colored("♻️ DNS cache flushed.", "cyan"))

def yt_access_menu():
    if not is_admin():
        print(colored("⚠️ To access this feature. Please run this script as an administrator (Windows) or use sudo (macOS/Linux).", "yellow"))
        return
    
    choice = input(colored("Do you want to (1) Block or (2) Unblock YouTube? Enter 1 or 2: ", "cyan"))
    if choice == "1":
        block_youtube()
        flush_dns()
    elif choice == "2":
        unblock_youtube()
        flush_dns()
    else:
        print(colored("❌ Invalid choice. Please enter 1 or 2.", "red"))

if __name__ == "__main__":
    yt_access_menu()
