#!/bin/bash

# View logs for all services or specific service

if [ -z "$1" ]; then
    echo "📋 Viewing logs for all services (Ctrl+C to exit)..."
    docker compose logs -f
else
    echo "📋 Viewing logs for $1 (Ctrl+C to exit)..."
    docker compose logs -f $1
fi
