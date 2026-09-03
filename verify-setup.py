#!/usr/bin/env python3
"""
Verify that the local setup is complete and working.
This script checks all components are installed and accessible.
"""

import subprocess
import sys
import os
from pathlib import Path

# Colors for terminal output
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"

def print_header(text):
    print(f"\n{BLUE}{'='*50}{RESET}")
    print(f"{BLUE}{text}{RESET}")
    print(f"{BLUE}{'='*50}{RESET}\n")

def print_ok(text):
    print(f"{GREEN}✅ {text}{RESET}")

def print_error(text):
    print(f"{RED}❌ {text}{RESET}")

def print_warning(text):
    print(f"{YELLOW}⚠️  {text}{RESET}")

def run_command(cmd, silent=True):
    """Run a command and return success/failure."""
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=silent,
            text=True,
            timeout=5
        )
        return result.returncode == 0
    except Exception:
        return False

def main():
    print_header("Verifying AI Options Trading Platform Setup")

    all_good = True

    # ========================================================================
    # Check Python
    # ========================================================================
    print(f"{BLUE}1. Python Installation{RESET}")

    if run_command("python3.11 --version"):
        try:
            version = subprocess.check_output("python3.11 --version", shell=True, text=True)
            print_ok(f"Python: {version.strip()}")
        except:
            print_error("Python 3.11+ not found")
            all_good = False
    else:
        print_error("Python 3.11+ not found")
        all_good = False

    # Check pip
    if run_command("pip --version"):
        try:
            version = subprocess.check_output("pip --version", shell=True, text=True)
            print_ok(f"pip: {version.strip()}")
        except:
            pass

    # ========================================================================
    # Check Virtual Environment
    # ========================================================================
    print(f"\n{BLUE}2. Virtual Environment{RESET}")

    venv_path = Path("venv")
    if venv_path.exists():
        print_ok("Virtual environment exists")

        # Check if packages are installed
        try:
            import fastapi
            print_ok("FastAPI installed")
        except ImportError:
            print_warning("FastAPI not installed - run: pip install -r requirements.txt")
            all_good = False
    else:
        print_error("Virtual environment not found")
        print_warning("Run: python3.11 -m venv venv")
        all_good = False

    # ========================================================================
    # Check Database
    # ========================================================================
    print(f"\n{BLUE}3. PostgreSQL Database{RESET}")

    if run_command("psql --version"):
        try:
            version = subprocess.check_output("psql --version", shell=True, text=True)
            print_ok(f"PostgreSQL: {version.strip()}")
        except:
            pass

        # Check if service is running
        if run_command("psql -U postgres -c 'SELECT 1'"):
            print_ok("PostgreSQL service is running")

            # Check if database exists
            result = subprocess.run(
                "psql -U postgres -lqt | grep -c options_trading",
                shell=True,
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                print_ok("Database 'options_trading' exists")
            else:
                print_warning("Database 'options_trading' not found")
                print_warning("Run: python scripts/init_db.py")
                all_good = False
        else:
            print_error("PostgreSQL service is not running")
            print_warning("Start PostgreSQL and try again")
            all_good = False
    else:
        print_error("PostgreSQL not found")
        print_warning("Install PostgreSQL 15+ and try again")
        all_good = False

    # ========================================================================
    # Check Redis
    # ========================================================================
    print(f"\n{BLUE}4. Redis Cache{RESET}")

    if run_command("redis-cli ping"):
        print_ok("Redis is running")
    else:
        print_warning("Redis is not running or not installed")
        print_warning("This is optional but recommended")

    # ========================================================================
    # Check Configuration
    # ========================================================================
    print(f"\n{BLUE}5. Configuration{RESET}")

    env_path = Path(".env")
    if env_path.exists():
        print_ok(".env file exists")

        # Check critical settings
        with open(".env") as f:
            content = f.read()

            if "PAPER_TRADING=true" in content:
                print_ok("Paper trading is ENABLED (default)")
            else:
                print_warning("Paper trading may be disabled")
                all_good = False

            if "LIVE_TRADING_ENABLED=false" in content:
                print_ok("Live trading is DISABLED (default)")
            else:
                print_error("Live trading is ENABLED - this is dangerous!")
                all_good = False
    else:
        print_warning(".env file not found")
        print_warning("Run: cp .env.example .env")

    # ========================================================================
    # Check Project Files
    # ========================================================================
    print(f"\n{BLUE}6. Project Files{RESET}")

    required_files = [
        "backend/main.py",
        "backend/config/settings.py",
        "backend/db/models.py",
        "backend/market_data/base.py",
        "backend/market_data/simulator.py",
        "requirements.txt",
        ".env.example",
    ]

    missing = []
    for file in required_files:
        if Path(file).exists():
            print_ok(f"✓ {file}")
        else:
            print_error(f"✗ {file}")
            missing.append(file)
            all_good = False

    if not missing:
        print_ok("All project files present")

    # ========================================================================
    # Summary
    # ========================================================================
    print_header("Verification Summary")

    if all_good:
        print_ok("Setup verification PASSED!")
        print("\nYou can now start the application:")
        print(f"  {BLUE}./start-local.sh{RESET} (Linux/macOS)")
        print(f"  {BLUE}.\\start-local.ps1{RESET} (Windows)")
        print("\nThen access:")
        print(f"  {BLUE}http://localhost:8000/api/docs{RESET}")
        return 0
    else:
        print_error("Setup verification FAILED!")
        print("\nPlease fix the issues above and run this script again:")
        print(f"  {BLUE}python verify-setup.py{RESET}")
        return 1

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print(f"\n{YELLOW}Cancelled{RESET}")
        sys.exit(1)
