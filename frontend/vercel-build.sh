#!/bin/bash
set -e

echo "Starting build process..."
echo "Current directory: $(pwd)"
echo "Contents of current directory:"
ls -la

echo "Changing to frontend directory..."
cd frontend

echo "Contents of frontend directory:"
ls -la

echo "Contents of frontend/public directory:"
ls -la public/

echo "Installing dependencies..."
npm install

echo "Building the app..."
npm run build

echo "Build completed successfully!"
echo "Contents of build directory:"
ls -la build/ 