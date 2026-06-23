import os
import sys
import sqlite3
import time
import urllib.request
import json

# Force instant unbuffered terminal printing
sys.stdout.reconfigure(line_buffering=True)

def generate_web_dashboard():
    """Reads your local corporate_ledger.db files and compiles a skinned HTML interface layout."""
    print("📊 Compiling Live Performance Portfolio Dashboard HTML using custom skin config...")
    try:
        skin_path = "dashboard_skin.json"
        if os.path.exists(skin_path):
            with open(skin_path, "r") as f:
                skin = json.load(f)
        else:
            skin = {
                "styles": {
                    "background_color": "#0a0e14", 
                    "primary_text_color": "#00ff66", 
                    "secondary_text_color": "#ffffff", 
                    "card_background": "#101720", 
                    "font_family": "monospace"
                }, 
                "components": {
                    "system_logs_header": "System Logs", 
                    "marketing_logs_header": "Marketing Logs"
                }
            }

        st = skin["styles"]
        comp = skin["components"]

        conn = sqlite3.connect('corporate_ledger.db')
        cursor = conn.cursor()
        cursor.execute("SELECT id, timestamp, event_type, message FROM system_logs ORDER BY id DESC LIMIT 10")
        system_rows = cursor.fetchall()
        cursor.execute("SELECT id, timestamp, keyword_targeted, output_file, status FROM marketing_ledger ORDER BY id DESC")
        marketing_rows = cursor.fetchall()
        conn.close()

        sys_logs_html = ""
        for row in system_rows:
            row_id, timestamp, event_type, message = row
            time_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(timestamp)))
            sys_logs_html += f"<tr><td>{row_id}</td><td>{time_str}</td><td><span class='badge'>{event_type}</span></td><td>{message}</td></tr>"

        mkt_logs_html = ""
        for row in marketing_rows:
            row_id, timestamp, keyword, output_file, status = row
            time_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(timestamp)))
            mkt_logs_html += f"<tr><td>{row_id}</td><td>{time_str}</td><td>#{keyword}</td><td><code>{output_file}</code></td><td><span class='badge'>{status}</span></td></tr>"

        html_template = f"""<!DOCTYPE html>
<html>
<head>
    <title>Autonomous Data Refinery Matrix - Skinned Dashboard</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {{ background: {st['background_color']}; color: {st['primary_text_color']}; font-family: {st['font_family']}; padding: 20px; }}
        .container {{ max-width: 1200px; margin: 0 auto; }}
        h1, h2 {{ border-bottom: 2px solid {st['primary_text_color']}; padding-bottom: 10px; color: {st['secondary_text_color']}; }}
        table {{ width: 100%; border-collapse: collapse; margin: 20px 0; background: {st['card_background']}; }}
        th, td {{ border: 1px solid {st['primary_text_color']}33; padding: 12px; text-align: left; }}
        th {{ background: #161b22; color: {st['secondary_text_color']}; }}
        .badge {{ background: {st['primary_text_color']}; color: #000; padding: 2px 6px; font-weight: bold; border-radius: 4px; }}
        code {{ color: #00bfff; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>📊 Corporate Engine Management Matrix</h1>
        <p>System Runtime Status: <strong>ONLINE // SKINNED</strong></p>
        
        <h2>{comp['system_logs_header']}</h2>
        <table>
            <tr><th>ID</th><th>Timestamp</th><th>Event Type</th><th>Message Payload</th></tr>
            {sys_logs_html}
        </table>
        
        <h2>{comp['marketing_logs_header']}</h2>
        <table>
            <tr><th>ID</th><th>Timestamp</th><th>Keyword Targeted</th><th>Output Path</th><th>Status</th></tr>
            {mkt_logs_html}
        </table>
    </div>
</body>
</html>"""
        with open("dashboard.html", "w", encoding="utf-8") as f:
            f.write(html_template)
        print("✅ Skinned Dashboard written successfully to: ./dashboard.html")
    except Exception as e:
        print(f"⚠️ Dashboard skinning compilation aborted: {e}")

def ping_google_search_indexers(target_slug):
    """Pings open search sitemap engine gateways to register newly compiled markdown content."""
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
    raw_token = os.environ.get("TELEGRAM_BOT_TOKEN", "")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID", "")

    # Fixed: Validate using the local environment variables instead of obsolete globals
    if not raw_token or not chat_id:
        print("⚠️ Configuration Error: TELEGRAM environment tokens are missing from execution scope.")
        return

    if raw_token.lower().startswith("bot"):
        bot_token = raw_token[3:]
    else:
        bot_token = raw_token

    print(f"📣 Dispatching real-time corporate metrics payload to Telegram ID: {chat_id}")
    
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
        url = f"https://telegram.org{bot_token}/sendMessage"
        payload = json.dumps({
            "chat_id": str(chat_id),
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
