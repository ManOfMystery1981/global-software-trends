#!/usr/bin/env python3
from industry_standard_report import IndustryStandardReport
from data_collector_bot import MarketDataCollector
from economist_agent import SeniorEconomistAgent
from delivery_bot import dispatch_secure_fulfillment_package # Import the dispatcher

#!/usr/bin/env python3
print("DEBUG: Script started successfully.") # ADD THIS LINE
from industry_standard_report import IndustryStandardReport
# ... rest of your code

class LLMAnalystBot:
    """
    Master Orchestrator:
    1. Collects raw multi-asset data.
    2. Synthesizes an expert macroeconomic narrative.
    3. Renders the report.
    4. Dispatches the secure delivery package.
    """
    def __init__(self, target_email="dsull1981@gmail.com"):
        self.report_engine = IndustryStandardReport()
        self.collector = MarketDataCollector()
        self.economist = SeniorEconomistAgent()
        self.target_email = target_email

    def run(self):
        print("🚀 Orchestrator: Initiating full-spectrum intelligence sweep...")
        
        # 1. Harvest raw data
        intelligence = self.collector.get_market_intelligence()
        
        # 2. Structure the data
        playbook = []
        for cat, assets in intelligence.items():
            for ticker, data in assets.items():
                volume_delta = data['volume_24h'] / data['historical_avg_volume']
                trend = "BREAKOUT" if volume_delta > 1.8 else "STABLE"
                playbook.append({
                    "ticker": ticker,
                    "category": cat,
                    "price": data['price'],
                    "trend": trend,
                    "narrative": f"Momentum Shift: {ticker} exhibiting {volume_delta:.1f}x volume vs 30d avg." if trend == "BREAKOUT" else "Market conditions within normal liquidity variance."
                })
        
        # 3. Generate the Economist's Strategic Narrative
        print("🧠 Invoking Senior Economist Agent for trend synthesis...")
        expert_narrative = self.economist.synthesize_market_playbook(playbook)
        
        # 4. Render
        html_path, csv_path = self.report_engine.generate_report(playbook, expert_narrative)
        
        print(f"✅ Institutional Playbook Generated.")
        
        # 5. DELIVERY PHASE
        print(f"📦 Handing off to Delivery Agent for: {self.target_email}")
        try:
            # We pass the paths if your delivery agent needs to read them, 
            # or it simply triggers the logic inside your delivery_bot.py
            delivery_success = dispatch_secure_fulfillment_package(self.target_email)
            
            if delivery_success:
                print("🚚 Delivery confirmed: Institutional package sent.")
            else:
                print("⚠️ Delivery failed: Check audit logs.")
        except Exception as e:
            print(f"❌ Critical error during delivery: {e}")

if __name__ == "__main__":
    # You can pass the email as an arg or keep it as a default
    LLMAnalystBot().run()
