import requests
import threading

domain = 'youtube.com'

with open('subdomains.txt') as file:
    subdomains = file.read().splitlines()

discovered_subdomains = []

lock = threading.Lock()

def check_subdomain(subdomain):
    url = f'http://{subdomain}.{domain}'
    try:
        requests.get(url)
    except requests.exceptions.RequestException:
        pass
    else:
        print(f'[+] Discovered subdomain: ', url)
        with lock:
            discovered_subdomains.append(url)
    
threads = []

for subdomain in subdomains:
    t = threading.Thread(target=check_subdomain, args=(subdomain,))
    t.start()
    threads.append(t)

for t in threads:
    t.join()

with open("discovered_subdomains.txt", "w") as file:
    for subdomain in discovered_subdomains:
        print(subdomain, file=file)