#!/usr/bin/env python3

import socket
import threading
import argparse
import time

print(r'''
███████╗ ██████╗ █████╗ ███╗   ██╗   ██████╗ ██╗   ██╗
██╔════╝██╔════╝██╔══██╗████╗  ██║   ██╔══██╗╚██╗ ██╔╝
███████╗██║     ███████║██╔██╗ ██║   ██████╔╝ ╚████╔╝ 
╚════██║██║     ██╔══██║██║╚██╗██║   ██╔═══╝   ╚██╔╝  
███████║╚██████╗██║  ██║██║ ╚████║██╗██║        ██║   
╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝╚═╝        ╚═╝
''')

# Global shared resources
open_ports = []
ports_scanned = 0
lock = threading.Lock()  # Prevent race conditions on shared variables


def scan_port(ip, port, semaphore):
    """
    Attempts a TCP connection to a specific port.
    If the port is open, it is added to the global list.
    """

    global ports_scanned

    with semaphore:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.5)
            result = s.connect_ex((ip, port))

            if result == 0:
                # Use lock to avoid mixed output from multiple threads
                with lock:
                    print(f"[+] Port {port} is open")
                    open_ports.append(port)

            s.close()

        except Exception:
            pass

        # Increase scanned port counter safely
        with lock:
            ports_scanned += 1


def show_progress(total_ports):
    """
    Displays progress every 20 seconds until scanning is complete.
    """

    while ports_scanned < total_ports:
        time.sleep(20)
        with lock:
            print(f"[+] Progress: {ports_scanned}/{total_ports} ports scanned...")


def main():
    parser = argparse.ArgumentParser(description="Multithreaded TCP Port Scanner")
    parser.add_argument("-ip", "--ip", required=True, help="Target IP address")
    parser.add_argument("-p", "--ports", type=int, required=True, help="Maximum port range to scan (1-N)")
    parser.add_argument("-t", "--threads", type=int, default=100, help="Maximum number of concurrent threads")
    parser.add_argument("-o", "--output", help="Optional file to save scan results")

    args = parser.parse_args()

    ip = args.ip
    ports = args.ports
    max_threads = args.threads
    output_file = args.output

    # Initial scan message
    with lock:
        print(f"[+] Starting scan on {ip} using {max_threads} threads...")

    semaphore = threading.Semaphore(max_threads)
    threads = []

    start = time.time()

    # Background progress thread
    progress_thread = threading.Thread(target=show_progress, args=(ports,))
    progress_thread.daemon = True
    progress_thread.start()

    # Create worker threads
    for port in range(1, ports + 1):
        t = threading.Thread(target=scan_port, args=(ip, port, semaphore))
        threads.append(t)
        t.start()

    # Wait for all threads to finish
    for t in threads:
        t.join()

    end = time.time()

    with lock:
        print(f"\n[+] Scan completed in {end - start:.2f} seconds.")
        print(f"[+] Open ports detected: {sorted(open_ports)}")

    # Save results to file if specified
    if output_file:
        with open(output_file, "w") as f:
            for p in sorted(open_ports):
                f.write(f"Port {p} is open\n")

        with lock:
            print(f"[+] Results saved to {output_file}")


if __name__ == "__main__":
    main()
