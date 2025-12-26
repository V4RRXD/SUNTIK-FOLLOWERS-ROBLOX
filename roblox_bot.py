#!/usr/bin/env python3
"""
ROBLOX ACCOUNT CREATOR & AUTO-FOLLOW BOT
Version: 2.0
Developer: V4RRXD
For Educational Purposes Only
"""

import requests
import json
import time
import random
import string
import hashlib
import uuid
import threading
import logging
from datetime import datetime
from typing import Dict, List, Optional
from colorama import Fore, Style, init
import os
import sys

init(autoreset=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/roblox_bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class RobloxBot:
    def __init__(self):
        self.base_url = "https://auth.roblox.com"
        self.api_url = "https://users.roblox.com"
        self.friends_url = "https://friends.roblox.com"
        
        # User agents pool
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15',
            'Mozilla/5.0 (Linux; Android 10; SM-G973F) AppleWebKit/537.36',
            'RobloxStudio/WinInet',
            'RobloxApp/0.497.1.4970114 (Windows; Windows 10)'
        ]
        
        # Proxies list (will be loaded from file)
        self.proxies = []
        self.current_proxy_index = 0
        
        # Account storage
        self.created_accounts = []
        
    def load_proxies(self, filename: str = "proxies/proxies.txt") -> List[str]:
        """Load proxies from file"""
        proxies = []
        try:
            with open(filename, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        proxies.append(line)
            logger.info(f"Loaded {len(proxies)} proxies")
        except FileNotFoundError:
            logger.warning("No proxy file found. Using direct connection.")
            proxies = [None]  # No proxy
        return proxies
    
    def get_random_proxy(self) -> Optional[Dict]:
        """Get random proxy for rotation"""
        if not self.proxies:
            return None
        
        proxy_str = random.choice(self.proxies)
        if proxy_str is None:
            return None
        
        # Parse proxy format (supports http, socks4, socks5)
        if '://' in proxy_str:
            return {"http": proxy_str, "https": proxy_str}
        else:
            # Assume http://ip:port
            return {"http": f"http://{proxy_str}", "https": f"http://{proxy_str}"}
    
    def generate_username(self) -> str:
        """Generate random username"""
        adjectives = ["Cool", "Epic", "Pro", "Mega", "Super", "Ultra", "Dark", "Light"]
        nouns = ["Player", "Gamer", "Warrior", "Hunter", "Wizard", "Ninja", "King", "Queen"]
        numbers = random.randint(100, 9999)
        
        username = f"{random.choice(adjectives)}{random.choice(nouns)}{numbers}"
        return username
    
    def generate_password(self) -> str:
        """Generate strong password"""
        chars = string.ascii_letters + string.digits + "!@#$%^&*"
        password = ''.join(random.choice(chars) for _ in range(12))
        return password
    
    def generate_birthdate(self) -> str:
        """Generate birthdate (over 13 years old)"""
        year = random.randint(1990, 2008)
        month = random.randint(1, 12)
        day = random.randint(1, 28)
        return f"{year}-{month:02d}-{day:02d}"
    
    def generate_xcsrf_token(self, session: requests.Session) -> Optional[str]:
        """Generate X-CSRF token for Roblox API"""
        try:
            headers = {
                'User-Agent': random.choice(self.user_agents),
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            }
            
            response = session.post(
                f"{self.base_url}/v2/logout",
                headers=headers,
                timeout=10
            )
            
            if 'x-csrf-token' in response.headers:
                return response.headers['x-csrf-token']
        except:
            pass
        return None
    
    def create_account(self, proxy: Optional[Dict] = None) -> Optional[Dict]:
        """Create Roblox account with bypass techniques"""
        try:
            session = requests.Session()
            if proxy:
                session.proxies.update(proxy)
            
            # Generate account data
            username = self.generate_username()
            password = self.generate_password()
            birthdate = self.generate_birthdate()
            gender = random.randint(1, 3)  # 1=Male, 2=Female, 3=Other
            
            # Step 1: Get initial cookies
            headers = {
                'User-Agent': random.choice(self.user_agents),
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            }
            
            # Get CSRF token first
            csrf_token = self.generate_xcsrf_token(session)
            if csrf_token:
                headers['X-CSRF-TOKEN'] = csrf_token
            
            # Step 2: Create account request
            account_data = {
                "username": username,
                "password": password,
                "birthday": birthdate,
                "gender": gender,
                "isTosAgreementBoxChecked": True,
                "agreementIds": ["54d8a8f0-d9c8-4cf3-bd26-0cbf8af0bba3"],
                "captchaToken": "",
                "captchaProvider": "PROVIDER_ARKOSE_LABS"
            }
            
            # Bypass attempt: Use different endpoints
            endpoints = [
                f"{self.base_url}/v2/signup",
                "https://apis.roblox.com/auth/v2/signup",
                "https://accountsettings.roblox.com/v1/email"
            ]
            
            endpoint = random.choice(endpoints)
            
            response = session.post(
                endpoint,
                json=account_data,
                headers=headers,
                timeout=30
            )
            
            if response.status_code in [200, 201, 204]:
                logger.info(f"✅ Account created: {username}")
                
                # Save account details
                account_info = {
                    "username": username,
                    "password": password,
                    "birthdate": birthdate,
                    "gender": gender,
                    "proxy": proxy,
                    "cookies": session.cookies.get_dict(),
                    "created_at": datetime.now().isoformat(),
                    "user_id": None
                }
                
                # Try to get user ID
                try:
                    user_response = session.get(
                        f"{self.api_url}/v1/users/authenticated",
                        headers=headers,
                        timeout=10
                    )
                    if user_response.status_code == 200:
                        user_data = user_response.json()
                        account_info["user_id"] = user_data.get("id")
                        account_info["display_name"] = user_data.get("displayName")
                except:
                    pass
                
                # Save to file
                self.save_account(account_info)
                self.created_accounts.append(account_info)
                
                return account_info
            else:
                logger.error(f"❌ Account creation failed: {response.status_code}")
                logger.error(f"Response: {response.text}")
                
        except Exception as e:
            logger.error(f"❌ Error creating account: {str(e)}")
        
        return None
    
    def bypass_captcha_simulation(self):
        """Simulate captcha bypass (educational)"""
        # Note: Actual captcha solving requires external services
        # like 2Captcha, Anti-Captcha, or CapMonster
        
        methods = [
            "Using AI solving service",
            "Human verification farm",
            "Session reuse from verified accounts",
            "Headless browser with automation",
            "Mobile API endpoint bypass"
        ]
        
        logger.info(f"🛡️  Simulating captcha bypass: {random.choice(methods)}")
        time.sleep(random.uniform(1, 3))
        return "SIMULATED_CAPTCHA_TOKEN"
    
    def get_user_id(self, username: str, proxy: Dict = None) -> Optional[int]:
        """Get Roblox user ID from username"""
        try:
            session = requests.Session()
            if proxy:
                session.proxies.update(proxy)
            
            headers = {
                'User-Agent': random.choice(self.user_agents),
                'Accept': 'application/json'
            }
            
            response = session.get(
                f"{self.api_url}/v1/users/search",
                params={"keyword": username},
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("data"):
                    for user in data["data"]:
                        if user.get("name", "").lower() == username.lower():
                            return user.get("id")
        
        except Exception as e:
            logger.error(f"Error getting user ID: {e}")
        
        return None
    
    def send_friend_request(self, account: Dict, target_user_id: int) -> bool:
        """Send friend request from account to target"""
        try:
            session = requests.Session()
            if account.get("proxy"):
                session.proxies.update(account["proxy"])
            
            # Set cookies from account
            for key, value in account.get("cookies", {}).items():
                session.cookies.set(key, value)
            
            headers = {
                'User-Agent': random.choice(self.user_agents),
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            }
            
            # Get CSRF token
            csrf_token = self.generate_xcsrf_token(session)
            if csrf_token:
                headers['X-CSRF-TOKEN'] = csrf_token
            
            # Send friend request
            response = session.post(
                f"{self.friends_url}/v1/users/{target_user_id}/request-friendship",
                json={"friendshipOriginSourceType": 0},
                headers=headers,
                timeout=15
            )
            
            if response.status_code in [200, 201, 204]:
                logger.info(f"✅ Friend request sent from {account['username']}")
                return True
            else:
                logger.warning(f"⚠️  Friend request failed: {response.status_code}")
                
        except Exception as e:
            logger.error(f"❌ Error sending friend request: {e}")
        
        return False
    
    def mass_follow(self, target_username: str, account_count: int = 10):
        """Create accounts and mass follow target"""
        logger.info(f"🚀 Starting mass follow operation for @{target_username}")
        logger.info(f"📊 Target: Create {account_count} accounts")
        
        # Load proxies
        self.proxies = self.load_proxies()
        
        # Get target user ID
        logger.info(f"🔍 Finding target user ID...")
        target_user_id = self.get_user_id(target_username)
        
        if not target_user_id:
            logger.error(f"❌ Target user not found: {target_username}")
            return
        
        logger.info(f"🎯 Target user ID: {target_user_id}")
        
        # Create accounts and follow
        successful_accounts = 0
        successful_follows = 0
        
        for i in range(account_count):
            logger.info(f"\n📝 Creating account {i+1}/{account_count}")
            
            # Rotate proxy
            proxy = self.get_random_proxy()
            
            # Create account
            account = self.create_account(proxy)
            
            if account:
                successful_accounts += 1
                
                # Wait before following
                time.sleep(random.uniform(2, 5))
                
                # Send friend request
                if self.send_friend_request(account, target_user_id):
                    successful_follows += 1
                
                # Random delay between accounts
                delay = random.uniform(5, 15)
                time.sleep(delay)
            else:
                logger.warning(f"⚠️  Account creation failed, retrying...")
        
        # Summary
        logger.info(f"\n{'='*50}")
        logger.info(f"📊 OPERATION SUMMARY")
        logger.info(f"{'='*50}")
        logger.info(f"✅ Accounts created: {successful_accounts}/{account_count}")
        logger.info(f"✅ Friend requests sent: {successful_follows}/{successful_accounts}")
        logger.info(f"🎯 Target: @{target_username} (ID: {target_user_id})")
        logger.info(f"📁 Accounts saved to: accounts/ directory")
        logger.info(f"{'='*50}")
    
    def save_account(self, account: Dict):
        """Save account to JSON file"""
        try:
            os.makedirs("accounts", exist_ok=True)
            filename = f"accounts/{account['username']}_{int(time.time())}.json"
            
            # Remove proxy object if present
            save_account = account.copy()
            if 'proxy' in save_account:
                save_account['proxy'] = str(save_account['proxy'])
            
            with open(filename, 'w') as f:
                json.dump(save_account, f, indent=4, ensure_ascii=False)
            
            logger.info(f"💾 Account saved: {filename}")
            
        except Exception as e:
            logger.error(f"Error saving account: {e}")
    
    def load_accounts(self) -> List[Dict]:
        """Load all created accounts"""
        accounts = []
        try:
            if os.path.exists("accounts"):
                for filename in os.listdir("accounts"):
                    if filename.endswith('.json'):
                        with open(f"accounts/{filename}", 'r') as f:
                            account = json.load(f)
                            accounts.append(account)
        except:
            pass
        return accounts
    
    def create_proxy_file_template(self):
        """Create proxy file template"""
        os.makedirs("proxies", exist_ok=True)
        proxy_template = """# Add your proxies here (one per line)
# Format: protocol://ip:port or ip:port
# Examples:
# http://123.456.789.012:8080
# socks5://123.456.789.012:1080
# 123.456.789.012:3128

# Free proxy sources (use at your own risk):
# https://free-proxy-list.net
# https://www.sslproxies.org
# https://www.us-proxy.org

# Rotating/residential proxies recommended:
# Bright Data, Oxylabs, Smartproxy, GeoSurf

"""
        with open("proxies/proxies.txt", "w") as f:
            f.write(proxy_template)
        logger.info("📝 Proxy template created: proxies/proxies.txt")

def display_banner():
    """Display tool banner"""
    banner = f"""
{Fore.CYAN}╔══════════════════════════════════════════════════════════╗
{Fore.CYAN}║{Fore.YELLOW}         RO BLOX BOT CREATOR v2.0                     {Fore.CYAN}║
{Fore.CYAN}║{Fore.YELLOW}       Account Creator & Mass Follower                {Fore.CYAN}║
{Fore.CYAN}║{Fore.GREEN}            MADE BY V4RRXD                            {Fore.CYAN}║
{Fore.CYAN}║{Fore.WHITE}         Telegram: @V4RRXD                            {Fore.CYAN}║
{Fore.CYAN}╚══════════════════════════════════════════════════════════╝{Style.RESET_ALL}
    """
    print(banner)

def main():
    """Main function"""
    display_banner()
    
    print(f"{Fore.RED}⚠️  DISCLAIMER:{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}• This tool is for educational purposes only")
    print(f"• Creating fake accounts violates Roblox Terms of Service")
    print(f"• Using this tool may result in IP/account bans")
    print(f"• Use at your own risk{Style.RESET_ALL}")
    
    print(f"\n{Fore.CYAN}[?] Continue? (y/n):{Style.RESET_ALL} ", end="")
    if input().lower() != 'y':
        print(f"{Fore.YELLOW}[*] Exiting...{Style.RESET_ALL}")
        return
    
    # Initialize bot
    bot = RobloxBot()
    
    # Create proxy template if not exists
    if not os.path.exists("proxies/proxies.txt"):
        bot.create_proxy_file_template()
        print(f"\n{Fore.YELLOW}[!] Please add proxies to proxies/proxies.txt{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[*] Restart after adding proxies{Style.RESET_ALL}")
        return
    
    # Get target username
    print(f"\n{Fore.CYAN}[?] Enter target Roblox username:{Style.RESET_ALL} ", end="")
    target_username = input().strip()
    
    if not target_username:
        print(f"{Fore.RED}[!] Username required!{Style.RESET_ALL}")
        return
    
    # Get account count
    try:
        print(f"{Fore.CYAN}[?] Number of accounts to create (1-50):{Style.RESET_ALL} ", end="")
        account_count = int(input().strip())
        account_count = max(1, min(account_count, 50))  # Limit to 50
    except:
        account_count = 10
        print(f"{Fore.YELLOW}[*] Using default: 10 accounts{Style.RESET_ALL}")
    
    # Start operation
    print(f"\n{Fore.GREEN}[*] Starting operation...{Style.RESET_ALL}")
    print(f"{Fore.GREEN}[*] Target: @{target_username}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}[*] Accounts to create: {account_count}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}[*] This may take several minutes...{Style.RESET_ALL}")
    
    try:
        bot.mass_follow(target_username, account_count)
        
        # Show summary
        created_accounts = bot.load_accounts()
        print(f"\n{Fore.GREEN}✅ Operation completed!{Style.RESET_ALL}")
        print(f"{Fore.CYAN}📊 Total accounts created: {len(created_accounts)}{Style.RESET_ALL}")
        
        if created_accounts:
            print(f"\n{Fore.YELLOW}📋 Created accounts:{Style.RESET_ALL}")
            for i, acc in enumerate(created_accounts[:5], 1):
                print(f"  {i}. {acc['username']} - Created: {acc['created_at'][:19]}")
            
            if len(created_accounts) > 5:
                print(f"  ... and {len(created_accounts)-5} more")
        
        print(f"\n{Fore.CYAN}📁 Accounts saved in: ~/RobloxBot/accounts/{Style.RESET_ALL}")
        print(f"{Fore.CYAN}📄 Logs: ~/RobloxBot/logs/roblox_bot.log{Style.RESET_ALL}")
        
    except KeyboardInterrupt:
        print(f"\n{Fore.RED}[!] Operation interrupted by user{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}[!] Error: {str(e)}{Style.RESET_ALL}")
    
    print(f"\n{Fore.CYAN}{'='*50}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Thank you for using Roblox Bot Creator{Style.RESET_ALL}")
    print(f"{Fore.CYAN}Developer: V4RRXD | Telegram: @V4RRXD{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*50}{Style.RESET_ALL}")

if __name__ == "__main__":
    # Check if running in Termux
    if not os.path.exists('/data/data/com.termux'):
        print(f"{Fore.YELLOW}[!] Warning: This tool is optimized for Termux{Style.RESET_ALL}")
    
    main()
