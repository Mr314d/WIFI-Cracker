import os
import re
import subprocess
import itertools
import string
import sys

# Function to check if the device is rooted
def is_rooted():
    try:
        root_check = subprocess.check_output(['su', '-c', 'id'])
        if b'uid=0' in root_check:
            return True
        else:
            return False
    except subprocess.CalledProcessError:
        return False

# Function to scan for WiFi networks
def scan_wifi():
    networks = subprocess.check_output(['termux-wifi-scaninfo'])
    networks = networks.decode('ascii')
    ssid_list = re.findall('SSID: (.+)', networks)
    return ssid_list

# Function to retrieve WiFi passwords
def retrieve_password(ssid):
    try:
        password = subprocess.check_output(['termux-wifi-showpass', ssid])
        password = password.decode('ascii')
        return password.strip()
    except subprocess.CalledProcessError:
        return None

# Function to crack WiFi passwords using an advanced brute force method (for educational purposes only)
def crack_password(password):
    # Advanced brute force method (for educational purposes only)
    characters = string.ascii_letters + string.digits + string.punctuation
    attempts = itertools.product(characters, repeat=8)  # Assuming password length is 8
    for attempt in attempts:
        attempt = ''.join(attempt)
        if attempt == password:
            print(f"Password cracked: {attempt}")
            return attempt
    print("Failed to crack password.")
    return None

# Main function
def main():
    # Check if running in Termux
    if 'termux' not in os.environ.get('HOME', ''):
        print("Error: This script is intended to be run in Termux.")
        return

    # Check if device is rooted
    if not is_rooted():
        print("Error: Device is not rooted. Root access is required for WiFi password cracking.")
        return

    # Check Termux version
    termux_version = os.environ.get('TERMUX_VERSION', '')
    if not termux_version:
        print("Error: Termux is not installed or not running.")
        return

    # Scan for WiFi networks
    networks = scan_wifi()
    print("Available WiFi networks:")
    for index, ssid in enumerate(networks, start=1):
        print(f"{index}. {ssid}")

    # Select a network to crack
    try:
        choice = int(input("Enter the number of the network you want to crack: "))
        if choice < 1 or choice > len(networks):
            print("Invalid choice. Please select a valid network number.")
            return
        selected_ssid = networks[choice - 1]
    except ValueError:
        print("Invalid input. Please enter a number.")
        return

    # Retrieve password for the selected network
    password = retrieve_password(selected_ssid)
    if password:
        print(f"WiFi Network: {selected_ssid}, Password: {password}")
        print("Attempting to crack password...")
        cracked_password = crack_password(password)
        if cracked_password:
            print(f"Cracked password for network {selected_ssid}: {cracked_password}")
        else:
            print(f"Could not crack password for network {selected_ssid}")
    else:
        print(f"Could not retrieve password for network: {selected_ssid}")

if __name__ == "__main__":
    main()