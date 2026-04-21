#!/bin/bash
# Push the repository to GitHub
# Usage: ./push-to-github.sh YOUR_GITHUB_USERNAME

USERNAME=${1:-YOUR_USERNAME}
REPO_NAME="agentic-ai-linkedin-poster"

echo "Setting up GitHub remote..."
echo "Repository: $REPO_NAME"
echo "Username: $USERNAME"

# Add the remote
git remote add origin "https://github.com/$USERNAME/$REPO_NAME.git"

# Push to GitHub
git push -u origin main

echo ""
echo "Done! Repository pushed to: https://github.com/$USERNAME/$REPO_NAME"
