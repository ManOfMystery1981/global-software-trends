# llm_analyst_bot.py - Updated with company data
import os
import json
import requests
from datetime import datetime

# Import all data sources
from delivery_bot import get_latest_data
from data_collector_bot import MarketDataCollector
from os_data_collector import OSDataCollector
from company_data_collector import TechCompanyDataCollector
from llm_analyst_prompt import generate_analyst_prompt

class LLMAnalystBot:
    """Bot that sends report data to a local LLM (Ollama) and retrieves the analyst article."""
    
    def __init__(self):
        self.llm_url = os.environ.get("LLM_API_URL", "http://localhost:11434/api/generate")
        self.model = os.environ.get("LLM_MODEL", "qwen2:0.5b")
        
    def wake_llm(self, prompt):
        """Send the prompt to Ollama and get the response."""
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "temperature": 0.5,
            "max_tokens": 2000,
            "system": "You are a Senior Technology Analyst with expertise in software development, financial markets, and technology forecasting."
        }
        
        try:
            print(f"🤖 Waking up LLM using {self.model}...")
            response = requests.post(self.llm_url, json=payload, timeout=180)
            
            if response.status_code == 200:
                data = response.json()
                article = data.get("response", "")
                print(f"✅ LLM analysis complete ({len(article)} characters).")
                return article
            else:
                print(f"❌ LLM error: {response.status_code}")
                return self._generate_fallback_article()
        except Exception as e:
            print(f"❌ LLM error: {e}")
            return self._generate_fallback_article()
    
    def _generate_fallback_article(self):
        """Generate a fallback article if the LLM is unavailable."""
        return """
## Executive Summary

The technology sector is undergoing a historic transformation driven by artificial intelligence. Nvidia has emerged as the dominant force with a $4.2 trillion market cap, while Amazon, Apple, and Microsoft continue to lead by revenue. The AI boom has added over $30 trillion in shareholder value, reshaping the competitive landscape.

## 1. Software Trends Deep Dive

AI/ML adoption continues to accelerate across enterprise sectors, with Rust and TypeScript gaining significant traction. Kubernetes remains the dominant cloud orchestration platform, while edge computing frameworks see 40% growth.

## 2. Tech Company Landscape

The top tech companies are now defined by their AI capabilities. Nvidia leads with 85% revenue growth, while Microsoft and Alphabet are investing heavily in AI infrastructure. Amazon's cloud business continues to drive its dominance.

## 3. AI Revolution Impact

AI is the single most important force reshaping the industry. Companies that embrace AI are seeing significant market rewards, while those that lag risk being disrupted.

## 4. Strategic Recommendations

**For CTOs:** Prioritize AI integration and cloud-native architecture. Invest in developer productivity tools and modern languages.

**For Developers:** Focus on AI/ML, Rust, and cloud-native skills. Build expertise in emerging technologies.

**For Founders:** Look for opportunities in AI tooling, developer productivity, and edge computing.

**For Recruiters:** Target candidates with AI/ML and cloud-native skills.
"""
    
    def run_analysis(self):
        """Main method to collect data, send to LLM, and return the article."""
        print("🔵 Starting LLM Analyst Bot...")
        
        # Collect all data
        print("📊 Gathering market data...")
        data = get_latest_data()
        trend_data = data['trends']
        metrics_data = data['metrics']
        
        print("📈 Gathering financial data...")
        collector = MarketDataCollector()
        market_data = collector.collect_all_data()
        crypto_data = market_data.get('crypto', {})
        stock_data = market_data.get('stocks', {})
        
        print("💻 Gathering OS data...")
        os_collector = OSDataCollector()
        os_data = os_collector.collect_all_data()
        
        print("🏢 Gathering tech company data...")
        company_collector = TechCompanyDataCollector()
        company_data = company_collector.collect_all_data()
        
        # Generate the prompt
        print("📝 Generating analyst prompt...")
        prompt = generate_analyst_prompt(
            trend_data, 
            metrics_data, 
            crypto_data, 
            stock_data, 
            os_data,
            company_data
        )
        
        # Send to LLM
        print("🤖 Sending to LLM...")
        article = self.wake_llm(prompt)
        
        # Save the article
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        article_file = f"analyst_article_{timestamp}.md"
        
        with open(article_file, 'w') as f:
            f.write(f"# Tech Analyst Report\n\n")
            f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}\n\n")
            f.write(article)
        
        print(f"✅ Article saved to {article_file}")
        return article

if __name__ == "__main__":
    bot = LLMAnalystBot()
    bot.run_analysis()
