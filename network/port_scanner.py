import socket 
import concurrent.futures
import sys

RED = "\033[91m"
GREEN = "\033[92m"
RESET = "\033[0m"

def format_port_results(results):
    formatted_result = "Port Scan Results:\n"
    formatted_result += "{:<8} {:<15} {:<10}\n".format("Port", "Service", "Status")
    formatted_result += "-"*85 + "\n"
    for port, service, banner, status in results:
        if status:
            formatted_result += f"{RED}{port:<8} {service:<15} {'Open':<10}{RESET}\n"
            if banner:
                banner_lines = banner.split("\n")
                for line in banner_lines:
                    formatted_result += f"{GREEN}{''*8}{line}{RESET}\n"
    return formatted_result

def get_banner(sock):
    try:
        sock.settimeout(1)
        banner = sock.recv(1024).decode().strip()
        return banner
    except:
        return ""

def scan_port(target_ip, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((target_ip, port))
        if result == 0:
            try:
                service = socket.getservbyport(port, 'tcp')
            except:
                service = "Unknown"
            banner = get_banner(sock)
            return port, service, banner, True
        else:
            return port, "", "", False
    except socket.error:
        return port, "", "", False
    finally:
        sock.close()

def port_scan(target_port, start_port, end_port):
    target_ip = socket.gethostbyname(target_port)
    print(f"Scanning {target_ip} from {start_port} to {end_port}")
    result = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=400) as executor:
        futures = {executor.submit(scan_port, target_ip, port): port for port in range(start_port, end_port+1)}
        total_ports = end_port - start_port + 1
        for i, future in enumerate(concurrent.futures.as_completed(futures), start=1):
            port, service, banner, status = future.result()
            result.append((port, service, banner, status))
            sys.stdout.write(f"\rProgress: {i}/{total_ports} ports scanned")
            sys.stdout.flush()
    sys.stdout.write("\n")
    print(format_port_results(result))

    
if __name__ == "__main__":
    target_host = input("Enter target ip: ")
    start_port = int(input("Enter start port: "))
    end_port = int(input("Enter end port: "))
    
    port_scan(target_host, start_port, end_port)
