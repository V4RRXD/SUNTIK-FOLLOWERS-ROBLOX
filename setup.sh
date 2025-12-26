#!/data/data/com.termux/files/usr/bin/bash
# Roblox Bot Installer
# Developer: V4RRXD

clear
echo ""
echo "╔══════════════════════════════════════════════════╗"
echo "║         RO BLOX BOT CREATOR v2.0                 ║
echo "║           Account Creator & Follower             ║
echo "║              MADE BY V4RRXD                      ║
echo "║         Telegram: @V4RRXD                        ║
echo "╚══════════════════════════════════════════════════╝"
echo ""

echo "[*] Installing dependencies..."
pkg update -y && pkg upgrade -y
pkg install python git curl wget -y
pip install --upgrade pip
pip install requests colorama fake-useragent selenium

echo "[*] Setting up directories..."
mkdir -p ~/RobloxBot/{accounts,proxies,cookies,logs}
cd ~/RobloxBot

echo "[+] Installation complete!"
echo "[*] Run: python3 roblox_bot.py"
