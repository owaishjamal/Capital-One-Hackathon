#!/usr/bin/env bash
# Pre-deployment setup script

echo "Kisan.AI Render Deployment Setup"
echo "================================"

# Check if we're in the right directory
if [ ! -f "manage.py" ]; then
    echo "Error: Please run this script from the Django project root (where manage.py is located)"
    exit 1
fi

# Make build script executable
chmod +x build.sh

echo "✓ Made build.sh executable"

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "Initializing git repository..."
    git init
    echo "✓ Git repository initialized"
fi

# Add all files to git
git add .
echo "✓ Files added to git"

# Check for environment variables template
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "✓ Created .env file from template"
    echo "⚠️  Please edit .env file with your actual credentials before deploying"
fi

echo ""
echo "Setup complete! Next steps:"
echo "1. Edit .env file with your actual API keys and credentials"
echo "2. Commit your changes: git commit -m 'Prepare for Render deployment'"
echo "3. Push to GitHub: git push origin main"
echo "4. Follow the deployment guide in DEPLOYMENT.md"
echo ""
echo "Important: Never commit your .env file to Git!"
