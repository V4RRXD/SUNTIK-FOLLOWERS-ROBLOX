#!/usr/bin/env python3
"""
Auto Proxy Getter for Roblox Bot
"""

import requests
from bs4 import BeautifulSoup
import time

def get_free_proxies():
    """Get free proxies from public sources"""
    print("[*] Fetching free proxies...")
    
    proxies = []
    
    try:
        # Source 1: free-proxy-list.net
        url = "https://free-proxy-list.net/"
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        table = soup.find('table', {'class': 'table table-striped table-bordered'})
        if table:
            rows = table.find_all('tr')[1:50]  # Get first 50
            for row in rows:
                cols = row.find_all('td')
                if len(cols) >= 2:
                    ip = cols[0].text.strip()
                    port = cols[1].text.strip()
                    proxies.append(f"{ip}:{port}")
        
        print(f"[+] Got {len(proxies)} proxies from free-proxy-list")
        
    except Exception as e:
        print(f"[-] Error: {e}")
    
    # Save to file
    if proxies:
        with open('proxies.txt', 'w') as f:
            f.write("# Auto-fetched proxies\n")
            for proxy in proxies:
                f.write(f"{proxy}\n")
        
        print(f"[+] Saved {len(proxies)} proxies to proxies.txt")
    
    return proxies

if __name__ == "__main__":
    get_free_proxies()
