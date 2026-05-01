#!/usr/bin/env bash
# exit on error
set -o errexit

# Install Python dependencies for the backend
pip install -r backend/requirements.txt

# Install Node dependencies and build the React frontend
cd frontend
npm install
npm run build
cd ..

echo "Build Complete! Frontend is now ready in frontend/dist"
