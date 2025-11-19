#!/bin/bash
# Auto-load relevant skills when an agent is invoked

AGENT_NAME=$1

case $AGENT_NAME in
  "frontend-development")
    echo "Loading frontend skills: react-development, typescript-mastery, css-modern, nextjs-fullstack, performance-optimization..."
    ;;
  "backend-development")
    echo "Loading backend skills: nodejs-api-development, spring-boot-development, graphql-api-design, database-architecture, api-security..."
    ;;
  "mobile-development")
    echo "Loading mobile skills: android-kotlin-development, ios-swift-development, react-native-development, flutter-development..."
    ;;
  "devops-infrastructure")
    echo "Loading DevOps skills: docker-containerization, kubernetes-orchestration, aws-cloud-architecture, terraform-iac..."
    ;;
  "ai-data-science")
    echo "Loading AI/Data skills: ml-model-development, ai-agent-systems, python-development..."
    ;;
  "programming-languages")
    echo "Loading programming skills: python-development, java-enterprise, software-architecture..."
    ;;
  "architecture-management")
    echo "Loading architecture skills: software-architecture, system-design, security-engineering, database-optimization..."
    ;;
  *)
    echo "Agent $AGENT_NAME invoked"
    ;;
esac
