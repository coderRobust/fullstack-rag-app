#!/bin/bash

# Configuration
BACKUP_DIR="./backups"
DB_CONTAINER="rag-qa-db"
VECTOR_STORE_DIR="./backend/faiss_index"
DATE=$(date +%Y%m%d_%H%M%S)

# Create backup directory
mkdir -p "$BACKUP_DIR"

# Backup database
echo "Backing up database..."
docker exec $DB_CONTAINER pg_dump -U postgres rag_qa > "$BACKUP_DIR/db_backup_$DATE.sql"

# Backup vector store
echo "Backing up vector store..."
tar -czf "$BACKUP_DIR/vector_store_$DATE.tar.gz" -C "$(dirname "$VECTOR_STORE_DIR")" "$(basename "$VECTOR_STORE_DIR")"

# Cleanup old backups (keep last 7 days)
find "$BACKUP_DIR" -type f -mtime +7 -delete

echo "Backup completed successfully!" 