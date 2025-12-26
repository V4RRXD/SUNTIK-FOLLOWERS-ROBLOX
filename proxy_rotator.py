#!/usr/bin/env python3
"""
Proxy Rotator for Roblox Bot
"""

import requests
import random
import time
from typing import List, Dict

class ProxyRotator:
    def __init__(self):
        self.proxies = []
        self.working_proxies = []
        self.failed_proxies = []
        
    def load_proxies(self, filepath: str) -> List[str]:
        """Load proxies from file"""
        proxies = []
        try:
            with open(filepath, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        proxies.append(line)
        except:
            pass
        return proxies
    
    def test_proxy(self, proxy: str) -> bool:
        """Test if proxy is working"""
        try:
            proxies = {
                "http": f"http://{proxy}",
                "https": f"http://{proxy}"
            }
            
            response = requests.get(
                "http://httpbin.org/ip",
                proxies=proxies,
                timeout=10
            )
            
            if response.status_code == 200:
                return True
        except:
            pass
        return False
    
    def validate_proxies(self, proxy_list: List[str]):
        """Validate all proxies"""
        print(f"[*] Testing {len(proxy_list)} proxies...")
        
        for proxy in proxy_list:
            if self.test_proxy(proxy):
                self.working_proxies.append(proxy)
                print(f"✅ {proxy}")
            else:
                self.failed_proxies.append(proxy)
                print(f"❌ {proxy}")
        
        print(f"\n📊 Results: {len(self.working_proxies)} working, {len(self.failed_proxies)} failed")
    
    def get_random_working_proxy(self) -> str:
        """Get random working proxy"""
        if self.working_proxies:
            return random.choice(self.working_proxies)
        return None
    
    def rotate_proxy(self) -> Dict:
        """Get proxy for rotation"""
        proxy_str = self.get_random_working_proxy()
        if proxy_str:
            return {
                "http": f"http://{proxy_str}",
                "https": f"http://{proxy_str}"
            }
        return None
