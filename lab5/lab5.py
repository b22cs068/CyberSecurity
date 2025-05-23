import time

# Predefined credentials
USERNAME = "admin"
PASSWORD = "securepass"

# Dictionary to track failed attempts and block time
failed_attempts = {}
blocked_ips = {}

while True:
    ip = input("Enter your IP address (or type 'exit' to stop): ")
    if ip.lower() == 'exit':
        break
    
    # Check if IP is blocked
    if ip in blocked_ips and time.time() < blocked_ips[ip]:
        print(f"IP {ip} is blocked. Try again later.")
        continue
    
    # Reset block if time has passed
    if ip in blocked_ips and time.time() >= blocked_ips[ip]:
        del blocked_ips[ip]
        failed_attempts[ip] = 0
    
    if ip not in failed_attempts:
        failed_attempts[ip] = 0
    
    # Login process
    username = input("Enter username: ")
    password = input("Enter password: ")
    
    if username == USERNAME and password == PASSWORD:
        print(f"Login Successful for IP {ip}!")
        failed_attempts[ip] = 0  # Reset failed attempts on success
    else:
        failed_attempts[ip] += 1
        attempts_left = 3 - failed_attempts[ip]
        if attempts_left > 0:
            print(f"Invalid credentials. Attempts left: {attempts_left}")
        else:
            print(f"Too many failed attempts. IP {ip} is blocked for 30 seconds.")
            blocked_ips[ip] = time.time() + 30  # Block for 30 seconds
