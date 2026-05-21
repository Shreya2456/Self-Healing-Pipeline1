#!/bin/bash
# Continuous health monitoring with auto-restart

CONTAINER_NAME="self-healing-pipeline-app-1"

echo "🩺 Starting Health Check Monitor..."
echo "Monitoring container: $CONTAINER_NAME"

while true; do
    HEALTH=$(docker inspect --format='{{.State.Health.Status}}' $CONTAINER_NAME 2>/dev/null)
    
    if [ "$HEALTH" == "unhealthy" ]; then
        echo "⚠️  [$(date)] Container is UNHEALTHY! Restarting..."
        docker-compose restart app
        echo "✅ [$(date)] Container restarted successfully"
    elif [ "$HEALTH" == "healthy" ]; then
        echo "✅ [$(date)] Container is healthy"
    elif [ "$HEALTH" == "" ]; then
        echo "⚠️  [$(date)] Container not found. Starting..."
        docker-compose up -d
    fi
    
    sleep 30  # Check every 30 seconds
done