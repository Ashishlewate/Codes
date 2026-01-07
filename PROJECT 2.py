import re
from collections import defaultdict

LOG_FILE = "system.log"
FAILED_LOGIN_PATTERN = r"Failed password for .* from (\d+\.\d+\.\d+\.\d+)"

ip_attempts = defaultdict(int)

def analyze_logs():
    with open(LOG_FILE, "r") as file:
        for line in file:
            match = re.search(FAILED_LOGIN_PATTERN, line)
            if match:
                ip = match.group(1)
                ip_attempts[ip] += 1

def generate_report():
    print("\n🔐 Security Threat Report")
    print("-" * 30)
    for ip, count in ip_attempts.items():
        if count >= 5:
            print(f"⚠ Suspicious IP Detected: {ip} | Attempts: {count}")

if __name__ == "__main__":
    analyze_logs()
    generate_report()
