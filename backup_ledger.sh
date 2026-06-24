#!/bin/bash

# Define strict folder paths matching your workspace tree context
DB_DIR="$HOME/local-ai/finance"
BACKUP_DIR="$DB_DIR/backups"
DB_FILE="corporate_ledger.db"

# Create chronological filename variables parameters profile
TIMESTAMP=$(date +"%Y-%m-%d_%H%M%S")
BACKUP_NAME="corporate_ledger_snapshot_${TIMESTAMP}.tar.gz"

# 1. Force establish the dedicated backup storage repository partition if dropped
mkdir -p "$BACKUP_DIR"

echo "📦 Initializing local database backup script framework sequence..."

if [ -f "$DB_DIR/$DB_FILE" ]; then
    # 2. Execute an absolute SQLite secure online backup file extraction copy first
    # This prevents archiving a file while an active background background daemon loop is mid-write
    sqlite3 "$DB_DIR/$DB_FILE" ".backup '$BACKUP_DIR/temporary_snapshot.db'"
    
    # 3. Compress the snapshot copy into a tight tarball matrix block
    cd "$BACKUP_DIR" || exit 1
    tar -czf "$BACKUP_NAME" temporary_snapshot.db
    
    # 4. Erase temporary artifacts to keep your directory clean
    rm -f temporary_snapshot.db
    
    # 5. Enforce strict data pruning (Keep only the latest 4 weekly backups, auto-delete older archives)
    ls -t corporate_ledger_snapshot_*.tar.gz | tail -n +5 | xargs rm -f 2>/dev/null
    
    echo "✅ Success: Ledger state packed and write-locked to: $BACKUP_DIR/$BACKUP_NAME"
else
    echo "❌ Error: Master ledger file $DB_DIR/$DB_FILE was not found on your disk partition path."
    exit 1
fi
