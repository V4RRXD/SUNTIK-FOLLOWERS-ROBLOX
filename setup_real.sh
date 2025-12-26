#!/data/data/com.termux/files/usr/bin/bash
# Real Roblox Bot Setup

echo "[*] Installing Python and dependencies..."
pkg update -y && pkg upgrade -y
pkg install python -y
pip install requests

echo "[*] Creating necessary files..."
mkdir -p ~/RobloxRealBot
cd ~/RobloxRealBot

# Create proxies file
cat > proxies.txt << 'EOF'
# Add your proxies here
# Format: ip:port
# Example: 123.456.789.012:8080

# Get free proxies from:
# https://free-proxy-list.net
# https://www.sslproxies.org

# Recommended: Buy rotating proxies from:
# Bright Data, Oxylabs, Smartproxy
EOF

echo "[+] Setup complete!"
echo "[*] Edit proxies.txt with your proxies first!"
echo "[*] Then run: python3 real_roblox_bot.py"
