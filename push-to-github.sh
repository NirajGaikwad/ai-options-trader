#!/bin/bash

# ============================================================================
# Push to GitHub & Setup Workflows
# ============================================================================

set -e

echo "=========================================="
echo "Push to GitHub Script"
echo "=========================================="
echo ""

# Check if GitHub username is provided
if [ -z "$1" ]; then
    echo "Usage: ./push-to-github.sh <GITHUB_USERNAME>"
    echo ""
    echo "Example: ./push-to-github.sh johndoe"
    echo ""
    echo "Steps to get your GitHub username:"
    echo "  1. Go to github.com"
    echo "  2. Click your profile icon (top right)"
    echo "  3. Click 'Your profile'"
    echo "  4. Your username is in the URL: github.com/YOUR_USERNAME"
    echo ""
    exit 1
fi

GITHUB_USERNAME=$1
REPO_NAME="ai-options-trader"

echo "GitHub Username: $GITHUB_USERNAME"
echo "Repository: $REPO_NAME"
echo ""

# ========================================================================
# Step 1: Verify files
# ========================================================================

echo "Step 1: Verifying files..."
echo ""

REQUIRED_FILES=(
    ".github/workflows/deploy.yml"
    ".github/scripts/market_monitor.py"
    ".gitignore"
    "backend/main.py"
    "backend/config/settings.py"
    "backend/db/models.py"
    "docker-compose.yml"
    "requirements.txt"
    "README.md"
)

MISSING_FILES=0
for file in "${REQUIRED_FILES[@]}"; do
    if [ -f "$file" ]; then
        echo "✅ $file"
    else
        echo "❌ $file (MISSING)"
        MISSING_FILES=$((MISSING_FILES + 1))
    fi
done

echo ""

if [ $MISSING_FILES -gt 0 ]; then
    echo "❌ Missing $MISSING_FILES required files!"
    echo "Please ensure you're in the /c/Trade directory"
    exit 1
fi

echo "✅ All required files present"
echo ""

# ========================================================================
# Step 2: Initialize Git (if not already)
# ========================================================================

echo "Step 2: Initializing Git repository..."
echo ""

if [ ! -d ".git" ]; then
    echo "Initializing new repository..."
    git init
    echo "✅ Git initialized"
else
    echo "⚠️  Git repository already exists"
fi

echo ""

# ========================================================================
# Step 3: Configure Git
# ========================================================================

echo "Step 3: Configuring Git..."
echo ""

# Check if git user is configured
if ! git config user.name > /dev/null 2>&1; then
    echo "Git user not configured. Enter your details:"
    read -p "Name: " git_name
    read -p "Email: " git_email
    git config user.name "$git_name"
    git config user.email "$git_email"
    echo "✅ Git configured"
else
    echo "✅ Git already configured"
    echo "   Name: $(git config user.name)"
    echo "   Email: $(git config user.email)"
fi

echo ""

# ========================================================================
# Step 4: Check remote
# ========================================================================

echo "Step 4: Setting up remote..."
echo ""

REMOTE_URL="https://github.com/$GITHUB_USERNAME/$REPO_NAME.git"

if git remote get-url origin > /dev/null 2>&1; then
    CURRENT_REMOTE=$(git remote get-url origin)
    if [ "$CURRENT_REMOTE" != "$REMOTE_URL" ]; then
        echo "⚠️  Remote URL mismatch!"
        echo "Current: $CURRENT_REMOTE"
        echo "Expected: $REMOTE_URL"
        echo ""
        read -p "Update remote? (y/n) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            git remote remove origin
            git remote add origin "$REMOTE_URL"
            echo "✅ Remote updated"
        fi
    else
        echo "✅ Remote already configured correctly"
    fi
else
    echo "Adding remote..."
    git remote add origin "$REMOTE_URL"
    echo "✅ Remote added: $REMOTE_URL"
fi

echo ""

# ========================================================================
# Step 5: Add and commit
# ========================================================================

echo "Step 5: Adding and committing files..."
echo ""

# Check if there are changes
if git diff-index --quiet HEAD -- 2>/dev/null; then
    echo "⚠️  No changes to commit"
    echo "Repository is up to date"
else
    echo "Adding files..."
    git add .

    echo "Creating commit..."
    git commit -m "Initial commit: AI Options Trading Platform Phase 1

- FastAPI backend with 15+ endpoints
- PostgreSQL + TimescaleDB database (20 tables)
- Market data simulator
- Configuration management
- Docker containerization
- GitHub Actions CI/CD pipeline
- Daily market monitoring
- Comprehensive documentation"

    echo "✅ Files committed"
fi

echo ""

# ========================================================================
# Step 6: Rename branch
# ========================================================================

echo "Step 6: Preparing branch..."
echo ""

CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)

if [ "$CURRENT_BRANCH" != "main" ]; then
    echo "Renaming branch to 'main'..."
    git branch -M main
    echo "✅ Branch renamed to 'main'"
else
    echo "✅ Already on 'main' branch"
fi

echo ""

# ========================================================================
# Step 7: Push to GitHub
# ========================================================================

echo "Step 7: Pushing to GitHub..."
echo ""
echo "Repository URL: $REMOTE_URL"
echo ""
echo "⚠️  You may be prompted for GitHub credentials:"
echo "   - If using HTTPS: enter your GitHub username and personal access token"
echo "   - If using SSH: ensure SSH key is configured"
echo ""

git push -u origin main

echo ""
echo "✅ Code pushed to GitHub successfully!"
echo ""

# ========================================================================
# Step 8: Verify
# ========================================================================

echo "Step 8: Verifying push..."
echo ""

if git ls-remote --exit-code origin > /dev/null 2>&1; then
    echo "✅ Remote verified"

    # Get commit count
    COMMITS=$(git rev-list --count main)
    echo "✅ Pushed $COMMITS commit(s)"
else
    echo "⚠️  Could not verify remote"
fi

echo ""

# ========================================================================
# Summary
# ========================================================================

echo "=========================================="
echo "✅ PUSH COMPLETE!"
echo "=========================================="
echo ""
echo "Repository: https://github.com/$GITHUB_USERNAME/$REPO_NAME"
echo ""
echo "Next steps:"
echo ""
echo "1. Go to your repository:"
echo "   https://github.com/$GITHUB_USERNAME/$REPO_NAME"
echo ""
echo "2. Go to 'Actions' tab to see workflows running:"
echo "   https://github.com/$GITHUB_USERNAME/$REPO_NAME/actions"
echo ""
echo "3. Wait for workflows to complete:"
echo "   ✅ test-and-lint"
echo "   ✅ build-docker"
echo "   ✅ market-monitor"
echo "   ✅ deployment-check"
echo ""
echo "4. (Optional) Configure Slack notifications:"
echo "   Settings → Secrets → New secret"
echo "   Name: SLACK_WEBHOOK"
echo "   Value: <your slack webhook URL>"
echo ""
echo "5. Read: GITHUB_ONLY_SETUP.md"
echo ""
echo "=========================================="
echo ""
