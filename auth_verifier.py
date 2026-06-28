#!/usr/bin/env python3
"""
auth_verifier.py
Institutional Access Control Layer (A+ Compliance Tier)
- Executes thread-safe, optimized relational read operations on sqlite tables.
- Implements strict hierarchical access checking: Yearly All-Access inherits individual report visibility.
"""

import sqlite3
import logging
from datetime import datetime, timezone

logger = logging.getLogger("A_Plus_Auth_Verifier")
DB_FILE = "billing_ledger.db"

def verify_yearly_access(customer_id: str) -> bool:
    """
    Checks the user_entitlements table to see if the user has an active 
    yearly pass that has not expired yet based on current epoch time.
    """
    current_epoch = int(datetime.now(timezone.utc).timestamp())
    
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute("PRAGMA journal_mode=WAL;")
        conn.execute("PRAGMA busy_timeout=2000;")
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT yearly_access_active, yearly_access_until 
            FROM user_entitlements 
            WHERE customer_id = ?
        """, (customer_id,))
        
        row = cursor.fetchone()
        if not row:
            return False
            
        is_active, access_until = row
        # Access is valid if the active flag is set AND the current time is before expiration
        if is_active == 1 and access_until > current_epoch:
            return True
            
    return False

def verify_report_ownership(customer_id: str, report_id: str) -> bool:
    """
    Hierarchical Access Check:
    1. If the user has a valid Yearly All-Access pass, they can view ALL reports.
    2. Otherwise, check if they made a direct one-off purchase for this specific report.
    """
    # Rule 1: All-access pass holders bypass specific item checks
    if verify_yearly_access(customer_id):
        logger.info(f"🔓 ACCESS GRANTED: User [{customer_id}] holds active Yearly All-Access.")
        return True
        
    # Rule 2: Fall back to checking specific report receipt records
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute("PRAGMA journal_mode=WAL;")
        conn.execute("PRAGMA busy_timeout=2000;")
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT 1 FROM report_purchases 
            WHERE customer_id = ? AND report_product_id = ?
        """, (customer_id, report_id))
        
        has_purchase = cursor.fetchone() is not None
        if has_purchase:
            logger.info(f"🔓 ACCESS GRANTED: User [{customer_id}] purchased direct line-item [{report_id}].")
            return True
            
    logger.warning(f"🔒 ACCESS DENIED: User [{customer_id}] lacks credentials for report [{report_id}].")
    return False

if __name__ == "__main__":
    print("✅ Authorization Verification Module Compiled Natively.")
