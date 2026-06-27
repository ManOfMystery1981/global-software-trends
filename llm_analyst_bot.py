#!/usr/bin/env python3
from industry_standard_report import IndustryStandardReport
from data_collector_bot import MarketDataCollector
from economist_agent import SeniorEconomistAgent

class LLMAnalystBot:
    """
    Master Orchestrator:
    1. Collects raw multi-asset data.
    2. Synthesizes an expert macroeconomic narrative.
    3. Triggers the dual-format (HTML/CSV) rendering engine.
    """
    def __init__(self):
        self.report_engine = IndustryStandardReport()
        self.collector = MarketDataCollector()
        self.economist = SeniorEconomistAgent()

    def run(self):
        print("🚀 Orchestrator: Initiating full-spectrum intelligence sweep...")
        
        # 1. Harvest raw data
        intelligence = self.collector.get_market_intelligence()
        
        # 2. Structure the data for the Playbook (Filtering for analysis)
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
        
        # 4. Final Render (HTML + CSV)
        html_path, csv_path = self.report_engine.generate_report(playbook, expert_narrative)
        
        print(f"✅ Institutional Playbook Delivered:")
        print(f"   -> Visual Dashboard: {html_path}")
        print(f"   -> Quantitative Dataset: {csv_path}")

if __name__ == "__main__":
    LLMAnalystBot().run()
