#!/bin/bash

ENV_FILE=".env"
BACKUP_DIR=".env_backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# Ensure backup directory exists
mkdir -p "$BACKUP_DIR"

# Check if .env exists
if [ -f "$ENV_FILE" ]; then
    cp "$ENV_FILE" "$BACKUP_DIR/.env.$TIMESTAMP"
    echo "✅ .env backed up as $BACKUP_DIR/.env.$TIMESTAMP"
else
    echo "❌ No .env file found to back up."
fi
