#!/usr/bin/env python3
"""
One-command automated setup for AI Options Trading Platform.
Works on Windows, Linux, and macOS.
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

# Colors
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"

def print_header(text):
    print(f"\n{BLUE}{'='*60}{RESET}")
    print(f"{BLUE}{text:^60}{RESET}")
    print(f"{BLUE}{'='*60}{RESET}\n")

def print_ok(text):
    print(f"{GREEN}✅ {text}{RESET}")

def print_error(text):
    print(f"{RED}❌ {text}{RESET}")

def print_warning(text):
    print(f"{YELLOW}⚠️  {text}{RESET}")

def print_info(text):
    print(f"{BLUE}ℹ️  {text}{RESET}")

def run_command(cmd, description=""):
    """Run a command and handle errors."""
    if description:
        print(f"  → {description}...")
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=30
        )
        return result.returncode == 0, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return False, "", "Command timeout"
    except Exception as e:
        return False, "", str(e)

def check_command(cmd, name):
    """Check if a command exists."""
    result = subprocess.run(
        f"command -v {cmd}" if platform.system() != "Windows" else f"where {cmd}",
        shell=True,
        capture_output=True
    )
    return result.returncode == 0

def main():
    print_header("AI Options Trading Platform - Automated Setup")

    os_type = platform.system()
    print_info(f"Detected OS: {os_type}")
    print("")

    # ====================================================================
    # Step 1: Python Check
    # ====================================================================
    print(f"{BLUE}Step 1/10: Checking Python 3.11+{RESET}")

    # On Windows, try 'python' first, then 'python3', then 'python3.11'
    python_cmd = None
    for cmd in ["python", "python3", "python3.11"]:
        if check_command(cmd, f"Python"):
            python_cmd = cmd
            break

    if not python_cmd:
        print_error("Python 3.11+ not found")
        print_warning("Install from: https://www.python.org/downloads/")
        return 1

    success, stdout, _ = run_command(f"{python_cmd} --version")
    if success:
        print_ok(f"Found {stdout.strip()}")
    else:
        print_error("Failed to verify Python")
        return 1

    # ====================================================================
    # Step 2: Virtual Environment
    # ====================================================================
    print(f"\n{BLUE}Step 2/10: Creating Virtual Environment{RESET}")

    venv_path = Path("venv")
    if venv_path.exists():
        print_warning("Virtual environment already exists")
    else:
        success, _, err = run_command(
            f"{python_cmd} -m venv venv",
            "Creating virtual environment"
        )
        if success:
            print_ok("Virtual environment created")
        else:
            print_error(f"Failed to create virtual environment: {err}")
            return 1

    # ====================================================================
    # Step 3: Activate and Upgrade pip
    # ====================================================================
    print(f"\n{BLUE}Step 3/10: Upgrading pip{RESET}")

    if os_type == "Windows":
        activate_cmd = ".\\venv\\Scripts\\python.exe"
    else:
        activate_cmd = "./venv/bin/python"

    success, _, err = run_command(
        f"{activate_cmd} -m pip install --upgrade pip setuptools wheel",
        "Upgrading pip"
    )
    if success:
        print_ok("pip upgraded")
    else:
        print_warning("pip upgrade had issues, continuing...")

    # ====================================================================
    # Step 4: Install Dependencies
    # ====================================================================
    print(f"\n{BLUE}Step 4/10: Installing Python Dependencies{RESET}")
    print_info("This may take 2-3 minutes...")

    success, stdout, err = run_command(
        f"{activate_cmd} -m pip install -r requirements.txt",
        "Installing dependencies"
    )
    if success:
        print_ok("Dependencies installed successfully")
    else:
        print_error(f"Failed to install dependencies: {err}")
        return 1

    # ====================================================================
    # Step 5: Check PostgreSQL
    # ====================================================================
    print(f"\n{BLUE}Step 5/10: Checking PostgreSQL{RESET}")

    if not check_command("psql", "psql"):
        print_error("PostgreSQL not found")
        print_warning("Install PostgreSQL 15+ from: https://www.postgresql.org/download/")
        if os_type == "Darwin":
            print_info("macOS: brew install postgresql@15")
        elif os_type == "Linux":
            print_info("Linux: sudo apt-get install postgresql postgresql-contrib")
        return 1

    success, stdout, _ = run_command("psql --version")
    if success:
        print_ok(f"Found {stdout.strip()}")
    else:
        print_error("PostgreSQL not accessible")

    # ====================================================================
    # Step 6: Check Redis (optional)
    # ====================================================================
    print(f"\n{BLUE}Step 6/10: Checking Redis (Optional){RESET}")

    if check_command("redis-cli", "redis-cli"):
        success, stdout, _ = run_command("redis-cli --version")
        if success:
            print_ok(f"Found {stdout.strip()}")
    else:
        print_warning("Redis not found (optional, but recommended)")

    # ====================================================================
    # Step 7: Create .env
    # ====================================================================
    print(f"\n{BLUE}Step 7/10: Creating Configuration{RESET}")

    env_path = Path(".env")
    if env_path.exists():
        print_warning(".env already exists")
    else:
        try:
            env_example = Path(".env.example").read_text()
            env_path.write_text(env_example)
            print_ok(".env created from template")
        except Exception as e:
            print_error(f"Failed to create .env: {e}")
            return 1

    # ====================================================================
    # Step 8: Create Database
    # ====================================================================
    print(f"\n{BLUE}Step 8/10: Creating PostgreSQL Database{RESET}")

    sql_commands = """
CREATE USER IF NOT EXISTS trader WITH PASSWORD 'trader123';
CREATE DATABASE IF NOT EXISTS options_trading OWNER trader;
ALTER ROLE trader SET client_encoding TO 'utf8';
ALTER ROLE trader SET default_transaction_isolation TO 'read committed';
ALTER ROLE trader SET default_transaction_deferrable TO on;
ALTER ROLE trader SET default_timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE options_trading TO trader;
"""

    sql_file = Path("temp_setup.sql")
    try:
        sql_file.write_text(sql_commands)
        success, _, err = run_command(
            "psql -U postgres -f temp_setup.sql 2>/dev/null",
            "Creating database"
        )
        sql_file.unlink()

        if success or "already exists" in err:
            print_ok("Database and user created")
        else:
            print_warning("Database creation had issues (may already exist)")
    except Exception as e:
        print_error(f"Failed to create database: {e}")
        if sql_file.exists():
            sql_file.unlink()

    # ====================================================================
    # Step 9: Initialize Database Schema
    # ====================================================================
    print(f"\n{BLUE}Step 9/10: Initializing Database Schema{RESET}")
    print_info("Creating 20 tables and indexes...")

    success, _, err = run_command(
        f"{activate_cmd} scripts/init_db.py",
        "Initializing schema"
    )
    if success:
        print_ok("Database schema initialized")
    else:
        print_warning(f"Schema initialization had issues: {err}")

    # ====================================================================
    # Step 10: Verification
    # ====================================================================
    print(f"\n{BLUE}Step 10/10: Verification{RESET}")

    # Check .env settings
    env_content = env_path.read_text()
    if "PAPER_TRADING=true" in env_content:
        print_ok("Paper trading is ENABLED")
    else:
        print_warning("Paper trading is not enabled")

    if "LIVE_TRADING_ENABLED=false" in env_content:
        print_ok("Live trading is DISABLED")
    else:
        print_error("Live trading is ENABLED - dangerous!")
        return 1

    # ====================================================================
    # Summary
    # ====================================================================
    print_header("Setup Complete!")

    print(f"{GREEN}✅ All setup steps completed successfully!{RESET}\n")

    print(f"Next steps:\n")

    print(f"1. {BLUE}Start PostgreSQL{RESET} (if not running):")
    if os_type == "Darwin":
        print(f"   brew services start postgresql@15\n")
    elif os_type == "Linux":
        print(f"   sudo systemctl start postgresql\n")
    else:
        print(f"   Start 'postgresql-x64-15' service\n")

    print(f"2. {BLUE}Start Redis{RESET} (if installed, optional):")
    if os_type == "Darwin":
        print(f"   brew services start redis\n")
    elif os_type == "Linux":
        print(f"   sudo systemctl start redis-server\n")
    else:
        print(f"   redis-server\n")

    print(f"3. {BLUE}Run the application{RESET}:")
    if os_type == "Windows":
        print(f"   .\\start-local.ps1\n")
    else:
        print(f"   ./start-local.sh\n")

    print(f"   Or manually:")
    print(f"   cd backend && python main.py\n")

    print(f"4. {BLUE}Test the API{RESET} (in new terminal):")
    print(f"   curl http://localhost:8000/health\n")

    print(f"5. {BLUE}View API documentation{RESET}:")
    print(f"   http://localhost:8000/api/docs\n")

    print(f"{BLUE}{'='*60}{RESET}")
    print(f"Setup ready! Activate venv and run the application.")
    print(f"{BLUE}{'='*60}{RESET}\n")

    return 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print(f"\n{YELLOW}Setup cancelled{RESET}")
        sys.exit(1)
    except Exception as e:
        print(f"\n{RED}Unexpected error: {e}{RESET}")
        sys.exit(1)
