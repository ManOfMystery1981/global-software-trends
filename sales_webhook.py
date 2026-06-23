import json
import sqlite3
import time
import os
import sys
import urllib.request
import ecosystem_extensions

# Force instant unbuffered console output
sys.stdout.reconfigure(line_buffering=True)

def verify_and_process_webhook(raw_incoming_payload):
    """
    Intercepts the structural JSON transmission parameters sent post-transaction,
    logs the metrics inside the local partition ledger, and fires Telegram alerts.
    """
    print("📡 Sales Webhook Receiver intercepting data transmission...")
    try:
        # Load the payload string parameters into a dictionary matrix
        payload = json.loads(raw_incoming_payload)
        
        # 1. Structural extraction path based on Helio / MoonPay standard webhook schemas
        transaction_status = payload.get("status") or payload.get("event", "")
        
        # Verify the notification is an explicit success track before triggering fulfillment
        if "success" in transaction_status.lower() or "completed" in transaction_status.lower():
            # Safely extract dynamic metadata variables passed from your storefront script block
            meta_data = payload.get("metaData", {})
            customer_email = meta_data.get("customerEmail") or payload.get("customerEmail", "unknown_buyer@internal.com")
            amount_sol = payload.get("amount") or payload.get("totalAmount", 0.01)
            signature = payload.get("signature") or payload.get("transactionId", f"manual_sig_{int(time.time())}")
            token_mint = payload.get("tokenMint", "SOL_Native")
            
            print(f"💰 Confirmed Revenue Event! Signature: {signature}")
            print(f"📨 Extracted required delivery field email: {customer_email}")
            
            # 2. Write the verified transaction properties to your persistent ledger array
            conn = sqlite3.connect('corporate_ledger.db')
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR IGNORE INTO solana_ledger (signature, asset_type, amount, token_mint, timestamp)
                VALUES (?, ?, ?, ?, ?)
            """, (signature, "MARKET_INTELLIGENCE_MATRIX", float(amount_sol), token_mint, int(time.time())))
            conn.commit()
            conn.close()
            
            # 3. Log the system operation hook event
            ecosystem_extensions.generate_web_dashboard() # Regenerates the HTML file with the new row
            
            # 4. Buzz your handheld phone app terminal through your verified connection path
            ecosystem_extensions.push_telegram_sales_alert(amount_sol, customer_email)
            
            # 5. Fire your background background worker daemons to build and ship the report files
            print("⚙️ Spawning core Asset Refinery & Delivery pipelines for automated fulfillment...")
            subprocess.run(["python3", "asset_refinery_bot.py"])
            subprocess.run(["python3", "delivery_bot.py", customer_email])
            
            return True
        else:
            print(f"⚠️ Notification skipped. Event status parameter reflects non-payment state: {transaction_status}")
            return False
            
    except Exception as e:
        print(f"❌ Webhook Execution Interrupted: {e}")
        return False

if __name__ == "__main__":
    # Test simulation package block to verify database integration and notification loops
    dummy_payload = json.dumps({
        "status": "SUCCESS",
        "transactionId": f"sig_test_{int(time.time())}",
        "amount": 0.01,
        "customerEmail": "dsull1981@gmail.com",
        "tokenMint": "So11111111111111111111111111111111111111112"
    })
    
    # Run the validation check, loading variables from your terminal profile environment paths
    os.environ["TELEGRAM_BOT_TOKEN"] = os.environ.get("TELEGRAM_BOT_TOKEN", "")
    os.environ["TELEGRAM_CHAT_ID"] = os.environ.get("TELEGRAM_CHAT_ID", "8794514690")
    
    verify_and_process_webhook(dummy_payload)
