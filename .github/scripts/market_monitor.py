#!/usr/bin/env python3
"""
Market Monitor - GitHub Actions triggered market status check.
Runs daily via GitHub Actions scheduled workflow.

Detects:
- Market opening times (alert for platform startup)
- Market closing times (alert for position closure)
- Market status (open/closed)

Market Hours (IST - Asia/Kolkata):
- Monday-Friday: 09:15 - 15:30
"""

import os
import sys
from datetime import datetime
import pytz
import requests
import json

# ============================================================================
# Configuration
# ============================================================================

MARKET_TIMEZONE = pytz.timezone('Asia/Kolkata')
MARKET_OPEN_HOUR = 9
MARKET_OPEN_MINUTE = 15
MARKET_CLOSE_HOUR = 15
MARKET_CLOSE_MINUTE = 30

# ============================================================================
# Helper Functions
# ============================================================================

def get_current_time():
    """Get current time in market timezone."""
    return datetime.now(MARKET_TIMEZONE)

def is_market_open():
    """Check if market is currently open."""
    now = get_current_time()

    # Not open on weekends
    if now.weekday() >= 5:  # Saturday=5, Sunday=6
        return False

    # Check time
    current_time = (now.hour, now.minute)
    open_time = (MARKET_OPEN_HOUR, MARKET_OPEN_MINUTE)
    close_time = (MARKET_CLOSE_HOUR, MARKET_CLOSE_MINUTE)

    return open_time <= current_time < close_time

def is_market_about_to_open(minutes=60):
    """Check if market will open within N minutes."""
    now = get_current_time()

    # Not applicable on weekends
    if now.weekday() >= 5:
        return False

    # Check if today is a trading day
    current_time_minutes = now.hour * 60 + now.minute
    open_time_minutes = MARKET_OPEN_HOUR * 60 + MARKET_OPEN_MINUTE

    minutes_until_open = open_time_minutes - current_time_minutes

    return 0 < minutes_until_open <= minutes

def is_market_about_to_close(minutes=30):
    """Check if market will close within N minutes."""
    now = get_current_time()

    # Not applicable on weekends
    if now.weekday() >= 5:
        return False

    # Check if market is currently open
    if not is_market_open():
        return False

    current_time_minutes = now.hour * 60 + now.minute
    close_time_minutes = MARKET_CLOSE_HOUR * 60 + MARKET_CLOSE_MINUTE

    minutes_until_close = close_time_minutes - current_time_minutes

    return 0 < minutes_until_close <= minutes

# ============================================================================
# Notifications
# ============================================================================

def send_slack_notification(message, color="good"):
    """Send notification to Slack."""
    webhook = os.getenv('SLACK_WEBHOOK')
    if not webhook:
        print("⚠️  SLACK_WEBHOOK not set - skipping Slack notification")
        return False

    payload = {
        "attachments": [
            {
                "color": color,
                "title": "📊 AI Options Trading Platform - Market Status",
                "text": message,
                "footer": "GitHub Actions Market Monitor",
                "ts": int(datetime.now().timestamp())
            }
        ]
    }

    try:
        response = requests.post(webhook, json=payload, timeout=10)
        if response.status_code == 200:
            print(f"✅ Slack notification sent: {message[:50]}...")
            return True
        else:
            print(f"❌ Slack notification failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error sending Slack notification: {e}")
        return False

def print_github_output(key, value):
    """Print GitHub Actions output variable."""
    output_file = os.getenv('GITHUB_OUTPUT')
    if output_file:
        with open(output_file, 'a') as f:
            f.write(f"{key}={value}\n")
        print(f"📤 GitHub output: {key}={value}")

# ============================================================================
# Market Status Reporting
# ============================================================================

def log_market_status():
    """Log current market status."""
    now = get_current_time()
    open_status = "OPEN" if is_market_open() else "CLOSED"

    print("\n" + "="*70)
    print("MARKET STATUS REPORT")
    print("="*70)
    print(f"Current Time (IST):   {now.strftime('%Y-%m-%d %H:%M:%S %Z')}")
    print(f"Day of Week:          {now.strftime('%A')}")
    print(f"Market Status:        {open_status}")
    print(f"Market Hours:         09:15 - 15:30 IST (Mon-Fri)")
    print("="*70)

def get_action_items():
    """Get action items based on market status."""
    items = []

    if is_market_open():
        items.append("✅ Platform should be RUNNING and accepting trades")
        items.append("📊 Monitor live market data")
        items.append("🎯 Track open positions")

    elif is_market_about_to_open(minutes=60):
        minutes = get_minutes_until_open()
        items.append(f"⏰ Market opens in ~{minutes} minutes")
        items.append("🚀 START GitHub Codespace to run platform")
        items.append("📋 Review overnight news and prepare strategies")

    elif is_market_about_to_close(minutes=30):
        minutes = get_minutes_until_close()
        items.append(f"🔔 Market closes in ~{minutes} minutes")
        items.append("💾 Close open positions")
        items.append("📝 Log trades and P&L")

    else:
        items.append("🛑 Platform can be IDLE")
        items.append("📚 Review code and prepare for next market open")
        items.append("🔧 Deploy updates to GitHub")

    return items

def get_minutes_until_open():
    """Get minutes until market opens."""
    now = get_current_time()
    current_time_minutes = now.hour * 60 + now.minute
    open_time_minutes = MARKET_OPEN_HOUR * 60 + MARKET_OPEN_MINUTE
    return max(0, open_time_minutes - current_time_minutes)

def get_minutes_until_close():
    """Get minutes until market closes."""
    now = get_current_time()
    current_time_minutes = now.hour * 60 + now.minute
    close_time_minutes = MARKET_CLOSE_HOUR * 60 + MARKET_CLOSE_MINUTE
    return max(0, close_time_minutes - current_time_minutes)

# ============================================================================
# Main Logic
# ============================================================================

def main():
    """Main market monitor logic."""

    print("\n🔍 GitHub Actions Market Monitor Started...\n")

    # Log current status
    log_market_status()

    # Check market status and take action
    if is_market_open():
        print("\n🟢 MARKET IS OPEN")
        print("="*70)
        message = f"🟢 MARKET OPEN - Platform is active and trading\n\nTime: {get_current_time().strftime('%H:%M:%S IST')}"
        send_slack_notification(message, "good")
        print_github_output("market_status", "open")
        print_github_output("market_opening", "false")

    elif is_market_about_to_open(minutes=60):
        minutes = get_minutes_until_open()
        print(f"\n🟡 MARKET OPENING IN ~{minutes} MINUTES")
        print("="*70)
        message = f"🟡 MARKET OPENING SOON - Prepare platform\n\nMarket opens in: ~{minutes} minutes\n\nSteps:\n1. Open GitHub Codespace\n2. Run: python setup.py\n3. Run: ./start-local.sh\n4. Access: http://localhost:8000/api/docs"
        send_slack_notification(message, "warning")
        print_github_output("market_status", "about_to_open")
        print_github_output("market_opening", "true")

    elif is_market_about_to_close(minutes=30):
        minutes = get_minutes_until_close()
        print(f"\n🟠 MARKET CLOSING IN ~{minutes} MINUTES")
        print("="*70)
        message = f"🟠 MARKET CLOSING SOON - Close positions\n\nMarket closes in: ~{minutes} minutes\n\nActions:\n• Close open positions\n• Record trades and P&L\n• Prepare for market close"
        send_slack_notification(message, "warning")
        print_github_output("market_status", "about_to_close")
        print_github_output("market_opening", "false")

    else:
        print("\n🔴 MARKET IS CLOSED")
        print("="*70)
        next_open = "09:15 IST Monday" if get_current_time().weekday() == 4 else "09:15 IST tomorrow"
        message = f"🔴 MARKET CLOSED - Platform idle\n\nNext market open: {next_open}\n\nGood time to:\n• Review code\n• Deploy updates\n• Optimize strategies"
        send_slack_notification(message, "#808080")
        print_github_output("market_status", "closed")
        print_github_output("market_opening", "false")

    # Print action items
    print("\n📋 ACTION ITEMS:")
    print("-" * 70)
    for item in get_action_items():
        print(f"  {item}")

    # Print instructions for GitHub Codespaces
    print("\n💻 TO RUN PLATFORM IN GITHUB CODESPACES:")
    print("-" * 70)
    print("  1. Go to: https://github.com/${{ github.repository }}/codespaces")
    print("  2. Click 'Create codespace on main'")
    print("  3. Wait for setup (2-3 minutes)")
    print("  4. In terminal run:")
    print("     python setup.py")
    print("     ./start-local.sh")
    print("  5. Open: http://localhost:8000/api/docs")

    print("\n✅ Market monitor completed\n")
    print("="*70 + "\n")

    return 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        print(f"\n❌ Error in market monitor: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
