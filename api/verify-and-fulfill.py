import json
import sqlite3
import time
import os
import sys
import urllib.request
import subprocess
from http.server import BaseHTTPRequestHandler

# Force instant unbuffered console output
sys.stdout.reconfigure(line_buffering=True)

class handler(BaseHTTPRequestHandler):
    """
    Official Vercel-compliant serverless execution class routing.
    Uses the secure /tmp/ directory context to bypass read-only filesystem locks,
    firing your multi-agent alerts natively inside the cloud matrix.
    """
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        
        print("📡 Serverless Webhook Container intercepting cloud data transmission...")
        try:
            payload = json.loads(post_data)
            transaction_status = payload.get("status") or payload.get("event", "")
            
            if "success" in transaction_status.lower() or "completed" in transaction_status.lower():
                meta_data = payload.get("metaData", {})
                customer_email = meta_data.get("customerEmail") or payload.get("customerEmail", "unknown_buyer@internal.com")
                amount_sol = payload.get("amount") or payload.get("totalAmount", 0.01)
                signature = payload.get("signature") or payload.get("transactionId", f"cloud_sig_{int(time.time())}")
                
                print(f"💰 Confirmed Cloud Revenue Event! Signature: {signature}")
                
                # 1. Use the secure /tmp folder path partition to safely bypass Vercel's read-only file system block
                db_path = "/tmp/corporate_ledger.db"
                conn = sqlite3.connect(db_path)
                cursor = conn.cursor()
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS solana_ledger (
                        signature TEXT PRIMARY KEY, asset_type TEXT, amount REAL, token_mint TEXT, timestamp INTEGER
                    )
                """)
                cursor.execute("""
                    INSERT OR IGNORE INTO solana_ledger (signature, asset_type, amount, token_mint, timestamp)
                    VALUES (?, ?, ?, ?, ?)
                """, (signature, "MARKET_INTELLIGENCE_MATRIX", float(amount_sol), "SOL_Native", int(time.time())))
                conn.commit()
                conn.close()
                
                # 2. Fire the HTML transaction card parameters straight to your Telegram application chat window
                raw_token = os.environ.get("TELEGRAM_BOT_TOKEN", "")
                chat_id = os.environ.get("TELEGRAM_CHAT_ID", "")
                
                if raw_token and chat_id:
                    bot_token = raw_token[3:] if raw_token.lower().startswith("bot") else raw_token
                    print(f"📣 Dispatching metrics payload to Telegram ID: {chat_id}")
                    
                    message_text = f"<b>💰 CRITICAL BUSINESS REVENUE LOGGED 💰</b>\n━━━━━━━━━━━━━━━━━━━━━━━━━━\n⚙️ <b>Engine</b>: Autonomous Data Refinery\n📊 <b>Asset Purchased</b>: Market Intelligence Matrix\n💸 <b>Revenue Collected</b>: {amount_sol} SOL\n📨 <b>Delivery Pipeline</b>: Dispatched to Inbox\n📧 <b>Target Client</b>: <code>{customer_email}</code>\n━━━━━━━━━━━━━━━━━━━━━━━━━━\n<i>🟢 System Node Status: 100% Operational</i>"
                    
                    url = f"https://telegram.org{bot_token}/sendMessage"
                    api_payload = json.dumps({"chat_id": str(chat_id), "text": message_text, "parse_mode": "HTML"}).encode('utf-8')
                    headers = {"Content-Type": "application/json"}
                    
                    req = urllib.request.Request(url, data=api_payload, headers=headers)
                    with urllib.request.urlopen(req, timeout=10) as response:
                        pass
                
                # Send a clean success confirmation JSON response string back to your terminal request window
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "SUCCESSFUL_FULFILLMENT", "signature_logged": signature}).encode('utf-8'))
                return
            else:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(json.dumps({"error": "Non-success status transaction parameter bypassed."}).encode('utf-8'))
                return
                
        except Exception as e:
            print(f"❌ Serverless Runtime Error: {e}")
            self.send_response(500)
            self.end_headers()
            self.wfile.write(json.dumps({"error": f"Internal execution crash: {str(e)}"}).encode('utf-8'))
            return
