# PortScanner.py
A fast, multithreaded TCP port scanner written in Python, featuring live progress tracking, thread limiting, and optional output saving. Designed for ethical security testing and network auditing.
A high‑performance multithreaded TCP port scanner written in Python.
Designed for security students, pentesters, and network administrators who need a fast, lightweight, and efficient scanning tool.

Features

⚡ High‑speed multithreaded scanning

🎛 Adjustable thread limit to avoid overwhelming systems

📡 Scans any port range (1–N)

📊 Live progress updates every 20 seconds

📁 Optional output file to save results

🧵 Thread‑safe printing and shared state management

🧪 Built for ethical pentesting and network analysis

Usage
Basic scan
python3 hyperscan.py -ip 192.168.1.10 -p 1000

Limit threads
python3 hyperscan.py -ip 192.168.1.10 -p 65535 -t 200

Save results to file
python3 hyperscan.py -ip 10.10.10.5 -p 5000 -o open_ports.txt

Arguments
Flag	Description
-ip / --ip	Target IP address (required)
-p / --ports	Max port range to scan (1-N)
-t / --threads	Max concurrent threads (default: 100)
-o / --output	Optional output file
Example Output
[+] Starting scan on 192.168.1.10 using 200 threads...
[+] Port 22 is open
[+] Port 80 is open
[+] Progress: 1800/5000 ports scanned...
[+] Scan completed in 12.83 seconds.
[+] Open ports detected: [22, 80]
[+] Results saved to open_ports.txt

Requirements

No external modules required besides Python's standard library.

Disclaimer

This tool is for educational and ethical security testing purposes only.
Do not scan systems you do not own or have explicit permission to test.
