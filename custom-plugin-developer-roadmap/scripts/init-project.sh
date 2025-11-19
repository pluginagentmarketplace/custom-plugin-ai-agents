#!/bin/bash
# Initialize project structure based on technology

TECHNOLOGY=$1
PROJECT_NAME=$2

echo "Creating $PROJECT_NAME project for $TECHNOLOGY..."

case $TECHNOLOGY in
  "react"|"nextjs")
    echo "npx create-next-app@latest $PROJECT_NAME --typescript --tailwind --app"
    ;;
  "vue")
    echo "npm create vue@latest $PROJECT_NAME"
    ;;
  "nodejs"|"express")
    echo "mkdir -p $PROJECT_NAME/{src,tests}"
    echo "cd $PROJECT_NAME && npm init -y && npm install express"
    ;;
  "python"|"fastapi")
    echo "mkdir -p $PROJECT_NAME/{app,tests}"
    echo "cd $PROJECT_NAME && python -m venv venv && source venv/bin/activate && pip install fastapi uvicorn"
    ;;
  "flutter")
    echo "flutter create $PROJECT_NAME"
    ;;
  "android")
    echo "Use Android Studio: File > New > New Project > Empty Activity"
    ;;
  *)
    echo "mkdir -p $PROJECT_NAME"
    ;;
esac

echo "Project $PROJECT_NAME initialized!"
