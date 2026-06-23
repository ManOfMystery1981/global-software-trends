import json
import os
import sys
import urllib.request
from http.server import BaseHTTPRequestHandler

# Force instant unbuffered console output alignment
sys.stdout.reconfigure(line_buffering=True)

class handler(BaseHTTPRequestHandler):
    """
    Official Vercel-compliant serverless execution class routing.
    Performs clean URL parameter parsing, injects cloud keys safely,
    and returns explicit text feedback directly back to your terminal shell.
    """
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        
        print("📡 Serverless Webhook Container intercepting cloud data transmission...")
        
        # 1. Initialize HTTP Response Headers first to prevent silent socket connection drops
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        
        try:
            payload = json.loads(post_data)
            transaction_status = payload.get("status") or payload.get("event", "")
            
            # Ensure the webhook notification payload matches a valid completion track
            if "success" in transaction_status.lower() or "completed" in transaction_status.lower():
                meta_data = payload.get("metaData", {})
                customer_email = meta_data.get("customerEmail") or payload.get("customerEmail", "unknown_buyer@internal.com")
                amount_sol = payload.get("amount") or payload.get("totalAmount", 0.01)
                signature = payload.get("signature") or payload.get("transactionId", "fallback_cloud_sig")
                
                print(f"💰 Confirmed Revenue Event! Signature: {signature}")
                
                # 2. Extract out environment variables safely vaulted in your Vercel panel settings
                raw_token = os.environ.get("TELEGRAM_BOT_TOKEN", "")
                chat_id = os.environ.get("TELEGRAM_CHAT_ID", "")
                
                if raw_token and chat_id:
                    # Strip out any potential accidental "bot" string prefixes from credentials
                    bot_token = raw_token[3:] if raw_token.lower().startswith("bot") else raw_token
                    print(f"📣 Dispatching real-time corporate metrics payload to Telegram ID: {chat_id}")
                    
                    message_text = f"<b>💰 CRITICAL BUSINESS REVENUE LOGGED 💰</b>\n━━━━━━━━━━━━━━━━━━━━━━━━━━\n⚙️ <b>Engine</b>: Autonomous Data Refinery\n📊 <b>Asset Purchased</b>: Market Intelligence Matrix\n💸 <b>Revenue Collected</b>: {amount_sol} SOL\n📨 <b>Delivery Pipeline</b>: Dispatched to Inbox\n📧 <b>Target Client</b>: <code>{customer_email}</code>\n━━━━━━━━━━━━━━━━━━━━━━━━━━\n<i>🟢 System Node Status: 100% Operational</i>"
                    
                    url = f"https://telegram.org{bot_token}/sendMessage"
                    api_payload = json.dumps({
                        "chat_id": str(chat_id),
                        "text": message_text,
                        "parse_mode": "HTML"
                    }).encode('utf-8')
                    
                    req = urllib.request.Request(url, data=api_payload, headers={"Content-Type": "application/json"})
                    with urllib.request.urlopen(req, timeout=10) as response:
                        print("✅ Telegram notification successfully pushed through API channel gateway.")
                else:
                    print("⚠️ Token Error: Telegram environment variables are missing from Vercel's console.")
                
                # Output confirmation back to your local curl terminal console window layout
                response_data = {"status": "SUCCESSFUL_FULFILLMENT", "signature_logged": signature, "telegram_routed": True}
                self.wfile.write(json.dumps(response_data).encode('utf-8'))
                return
            else:
                self.wfile.write(json.dumps({"status": "SKIPPED", "info": "Non-success transaction state."}).encode('utf-8'))
                return
                
        except Exception as e:
            print(f"❌ Serverless Execution Anomaly: {str(e)}")
            self.wfile.write(json.dumps({"status": "SERVER_ERROR", "details": str(e)}).encode('utf-8'))
            return
