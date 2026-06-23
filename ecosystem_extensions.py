import os
import sys
import sqlite3
import time
import urllib.request
import json

# Force instant unbuffered terminal printing
sys.stdout.reconfigure(line_buffering=True)

# Secure environment variable ingestion
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

def generate_web_dashboard():
    """Reads your local corporate_ledger.db files and compiles a flat, zero-dependency static HTML file."""
    print("📊 Compiling Live Performance Portfolio Dashboard HTML...")
    try:
        conn = sqlite3.connect('corporate_ledger.db')
        cursor = conn.cursor()
        
        # Extract the latest process log data lines
        cursor.execute("SELECT id, timestamp, event_type, message FROM system_logs ORDER BY id DESC LIMIT 10")
        system_rows = cursor.fetchall()
        
        # Extract your compiled markdown marketing pages data lines
        cursor.execute("SELECT id, timestamp, keyword_targeted, output_file, status FROM marketing_ledger ORDER BY id DESC")
        marketing_rows = cursor.fetchall()
        conn.close()
        
        # Build dynamic HTML string injection arrays
        sys_logs_html = ""
        for row in system_rows:
            sys_logs_html += f"<tr><td>{row[0]}</td><td>{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(row[1]))}</td><td><span class='badge'>{row[2]}</span></td><td>{row[3]}</td></tr>"
            
        mkt_logs_html = ""
        for row in marketing_rows:
            mkt_logs_html += f"<tr><td>{row[0]}</td><td>{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(row[1]))}</td><td>#{row[2]}</td><td><code>{row[3]}</code></td><td><span class='success-badge'>{row[4]}</span></td></tr>"
            
        html_template = f"""<!DOCTYPE html>
<html>
<head>
    <title>Autonomous Data Refinery Matrix - Executive Dashboard</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {{ font-family: 'Courier New', monospace; background: #0a0e14; color: #00ff66; padding: 20px; }}
        .container {{ max-width: 1200px; margin: 0 auto; }}
        h1, h2 {{ border-bottom: 2px solid #00ff66; padding-bottom: 10px; color: #ffffff; }}
        table {{ width: 100%; border-collapse: collapse; margin: 20px 0; background: #101720; }}
        th, td {{ border: 1px solid #1f2f40; padding: 12px; text-align: left; }}
        th {{ background: #1a2330; color: #ffffff; }}
        .badge {{ background: #ffaa00; color: #000; padding: 2px 6px; font-weight: bold; border-radius: 3px; }}
        .success-badge {{ background: #00ff66; color: #000; padding: 2px 6px; font-weight: bold; border-radius: 3px; }}
        code {{ color: #00bfff; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>📊 Corporate Engine Management Matrix</h1>
        <p>System Runtime Status: <strong>ONLINE // OPERATIONAL</strong></p>
        
        <h2>📁 System Process Reconciliation Logs</h2>
        <table>
            <tr><th>ID</th><th>Timestamp</th><th>Event Type</th><th>Message Payload</th></tr>
            {sys_logs_html}
        </table>
        
        <h2>🎯 Autonomous Marketing Advertising Logs</h2>
        <table>
            <tr><th>ID</th><th>Timestamp</th><th>Keyword Targeted</th><th>Output Path</th><th>Status</th></tr>
            {mkt_logs_html}
        </table>
    </div>
</body>
</html>
"""
        with open("dashboard.html", "w", encoding="utf-8") as f:
            f.write(html_template)
        print("✅ Dashboard written successfully to: ./dashboard.html")
    except Exception as e:
        print(f"⚠️ Dashboard compilation aborted: {e}")

def ping_google_search_indexers(target_slug):
    """Pings open search sitemap engine gateways to register newly compiled markdown content with correct routing syntax."""
    # Fixed string formatting to append proper forward slashes and the .md file extension cleanly
    live_post_url = f"https://vercel.app{target_slug}.md"
    print(f"🕸️ Indexer broad-pinging search crawler infrastructure networks for link: {live_post_url}")
    try:
        ping_endpoint = f"http://google.com{live_post_url}"
        req = urllib.request.Request(ping_endpoint, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=8) as response:
            if response.status == 200:
                print(f"🚀 Success: Google indexing notification gateway accepted link parameter request.")
    except Exception as e:
        print(f"⚠️ Crawler registration delayed: {e}")

def push_telegram_sales_alert(amount_sol, customer_email):
    """Fires a high-priority HTML push notification payload directly to your personal user chat window ID."""
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("⚠️ Configuration Error: TELEGRAM environment tokens are missing from execution scope.")
        return

    print(f"📣 Dispatching real-time corporate metrics payload to Telegram ID: {TELEGRAM_CHAT_ID}")
    
    message_text = f"""
<b>💰 CRITICAL BUSINESS REVENUE LOGGED 💰</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━
⚙️ <b>Engine</b>: Autonomous Data Refinery
📊 <b>Asset Purchased</b>: Market Intelligence Matrix
💸 <b>Revenue Collected</b>: {amount_sol} SOL
📨 <b>Delivery Pipeline</b>: Dispatched to Inbox
📧 <b>Target Client</b>: <code>{customer_email}</code>
━━━━━━━━━━━━━━━━━━━━━━━━━━
<i>🟢 System Node Status: 100% Operational</i>
"""
    try:
        url = f"https://telegram.org{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = json.dumps({
            "chat_id": str(TELEGRAM_CHAT_ID),
            "text": message_text,
            "parse_mode": "HTML"
        }).encode('utf-8')
        
        headers = {"Content-Type": "application/json"}
        req = urllib.request.Request(url, data=payload, headers=headers)
        
        with urllib.request.urlopen(req, timeout=10) as response:
            res_data = json.loads(response.read().decode('utf-8'))
            if res_data.get("ok"):
                print("✅ Telegram notification successfully routed to operator handheld terminal device.")
            else:
                print(f"❌ Telegram API Failure: {res_data}")
    except Exception as e:
        print(f"⚠️ Telegram alert connection routing dropped: {e}")

if __name__ == "__main__":
    generate_web_dashboard()
    ping_google_search_indexers("solanametrics")
    push_telegram_sales_alert(0.01, "dsull1981@gmail.com")
