#!/bin/bash

# This script pushes your code to GitHub
# Run this on YOUR computer (not Emergent)

cd /path/to/your/local/repo

# Add remote (if not already added)
git remote add origin https://github.com/mvbinvestor-alt/Fno_Trading.git

# Add all files
git add .

# Commit
git commit -m "Add complete F&O trading system with documentation"

# Push
git push -u origin main

echo "✅ Pushed to GitHub!"
echo "📱 Now deploy to Railway for phone access:"
echo "   npm install -g @railway/cli"
echo "   railway login"
echo "   railway init"
echo "   railway up"
