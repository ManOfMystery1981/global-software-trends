#!/usr/bin/env python3
import sys
import time
import concurrent.futures
import requests

TARGET_URL = "http://127.0.0.1:8080"
TOTAL_BURST_REQUESTS = 100
CONCURRENT_THREADS = 15

def send_malicious_burst_packet(request_index: int) -> int:
    custom_headers = {
        "User-Agent": "A_Plus_Red_Team_Stress_Bot_v5",
        "X-Stress-Test-Index": str(request_index)
    }
    try:
        response = requests.get(TARGET_URL, headers=custom_headers, timeout=2)
        return response.status_code
    except requests.exceptions.RequestException:
        return 503

def run_stress_campaign():
    print(f"🔥 ATTACK SIMULATION STARTING: Flooding local target [{TARGET_URL}]...")
    print(f"📦 Total Load: {TOTAL_BURST_REQUESTS} requests | Concurrency Rails: {CONCURRENT_THREADS} workers\n")

    start_time = time.time()
    status_matrix = {}

    with concurrent.futures.ThreadPoolExecutor(max_workers=CONCURRENT_THREADS) as executor:
        results = executor.map(send_malicious_burst_packet, range(TOTAL_BURST_REQUESTS))
        for code in results:
            status_matrix[code] = status_matrix.get(code, 0) + 1

    duration = time.time() - start_time

    print("============== RED TEAM ATTACK METRICS ==============")
    print(f"⏱️ Total Campaign Duration: {duration:.4f} seconds")
    print(f"⚡ Processing Speed: {TOTAL_BURST_REQUESTS / duration:.2f} requests/sec")
    print("\n📊 HTTP Server Status Codes Logged:")
    for status, count in status_matrix.items():
        print(f"  -> Status Code [{status}]: {count} occurrences")

    if 503 in status_matrix or 500 in status_matrix:
        print("\n❌ SECURITY DEFECT DETECTED: The server leaked internal errors or dropped connections under load.")
        sys.exit(1)
    else:
        print("\n✅ SECURITY INTEGRITY SECURED: The server withstood the concurrency burst with zero errors.")

if __name__ == "__main__":
    run_stress_campaign()
