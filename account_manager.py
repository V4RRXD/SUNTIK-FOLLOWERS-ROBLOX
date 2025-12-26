#!/usr/bin/env python3
"""
Account Manager for Roblox Bot
"""

import json
import os
from typing import List, Dict

class AccountManager:
    def __init__(self):
        self.accounts_dir = "accounts"
        os.makedirs(self.accounts_dir, exist_ok=True)
    
    def save_account(self, account_data: Dict):
        """Save account to JSON file"""
        filename = f"{self.accounts_dir}/{account_data['username']}.json"
        with open(filename, 'w') as f:
            json.dump(account_data, f, indent=4)
    
    def load_accounts(self) -> List[Dict]:
        """Load all accounts"""
        accounts = []
        for filename in os.listdir(self.accounts_dir):
            if filename.endswith('.json'):
                with open(f"{self.accounts_dir}/{filename}", 'r') as f:
                    accounts.append(json.load(f))
        return accounts
    
    def get_account_stats(self) -> Dict:
        """Get account statistics"""
        accounts = self.load_accounts()
        return {
            "total_accounts": len(accounts),
            "with_user_id": len([a for a in accounts if a.get("user_id")]),
            "recent_accounts": sorted(accounts, key=lambda x: x.get("created_at", ""), reverse=True)[:5]
        }
