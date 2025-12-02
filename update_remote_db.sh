#!/bin/bash

# This script updates the database schema on the remote server
# Run this after git pull and docker compose up -d

echo "🚀 Updating database schema..."

# Add 'link' column to 'areas' table if it doesn't exist
docker compose exec postgres psql -U postgres -d hedri_sakni -c "ALTER TABLE areas ADD COLUMN IF NOT EXISTS link VARCHAR(500);"

if [ $? -eq 0 ]; then
    echo "✅ Database updated successfully!"
else
    echo "❌ Failed to update database. Make sure the postgres container is running."
fi
