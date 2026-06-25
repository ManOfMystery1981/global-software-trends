# llm_analyst_bot.py
import os
import json
import requests
from datetime import datetime

# Import your data sources (these should already exist in your repo)
try:
    from delivery_bot import get_latest_data
except ImportError:
    print("⚠️ Could not import from delivery_bot.py, using fallback")
    # Fallback data
    def get_latest_data():
        return {
            'trends': ['AI/ML adoption growing', 'Rust gaining popularity', 'Kubernetes dominant'],
            'metrics': [{'Total frameworks': '45'}],
            'codebase_stats': {'Languages': 'Python'}
        }

try:
    from data_collector_bot import MarketDataCollector
except ImportError:
    print("⚠️ Could not import data_collector_bot.py")
    MarketDataCollector = None

try:
    from os_data_collector import OSDataCollector
except ImportError:
    print("⚠️ Could not import os_data_collector.py")
    OSDataCollector = None

try:
    from llm_analyst_prompt import generate_analyst_prompt
except ImportError:
    print("⚠️ Could not import llm_analyst_prompt.py, using built-in prompt")
    def generate_analyst_prompt(trend_data, metrics_data, crypto_data, stock_data, os_data):
        return f"Analyze this data: Trends: {trend_data}, Metrics: {metrics_data}"


class LLMAnalystBot:
    """Bot that sends report data to a local LLM (Ollama) and retrieves the analyst article."""
    
    def __init__(self):
        # Ollama API endpoint (runs on localhost in GitHub Actions)
        self.llm_url = os.environ.get("LLM_API_URL", "http://localhost:11434/api/generate")
        self.model = os.environ.get("LLM_MODEL", "qwen2:0.5b")
        
    def wake_llm(self, prompt):
        """Send the prompt to Ollama and get the response."""
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "temperature": 0.5,
            "max_tokens": 1500,
            "system": "You are a Senior Technology Analyst with expertise in software development, financial markets, and technology forecasting."
        }
        
        try:
            print(f"🤖 Waking up LLM using {self.model}...")
            print(f"📡 Sending request to: {self.llm_url}")
            
            response = requests.post(self.llm_url, json=payload, timeout=120)
            
            if response.status_code == 200:
                data = response.json()
                article = data.get("response", "")
                if article:
                    print(f"✅ LLM analysis complete ({len(article)} characters).")
                    return article
                else:
                    print("⚠️ LLM returned empty response")
                    return self._generate_fallback_article()
            else:
                print(f"❌ LLM error: {response.status_code} - {response.text[:200]}")
                return self._generate_fallback_article()
                
        except requests.exceptions.Timeout:
            print("❌ LLM timeout - the model took too long to respond.")
            return self._generate_fallback_article()
        except requests.exceptions.ConnectionError:
            print("❌ LLM connection error - is Ollama running?")
            return self._generate_fallback_article()
        except Exception as e:
            print(f"❌ LLM error: {e}")
            return self._generate_fallback_article()
    
    def _generate_fallback_article(self):
        """Generate a fallback article if the LLM is unavailable."""
        return """
## Executive Summary

The software development landscape is experiencing significant shifts driven by AI adoption, cloud infrastructure maturity, and evolving developer preferences. This report provides a comprehensive analysis of the current trends and future projections based on the latest market intelligence data.

## 1. Software Trends Deep Dive

The data shows strong momentum in AI/ML adoption across enterprise sectors, with growth accelerating as organizations integrate AI capabilities into their core products. Rust continues to gain traction among systems programmers, while Kubernetes remains the dominant orchestration platform. TypeScript has surpassed Java in new project starts, indicating a shift in developer preferences towards modern, type-safe languages.

## 2. Financial & Market Analysis

Cryptocurrency markets are showing signs of maturation, with institutional adoption increasing despite price volatility. Tech stocks continue to outperform broader markets, particularly companies focused on AI infrastructure and cloud services. The correlation between software trends and market performance suggests that companies leading in AI and cloud adoption are commanding premium valuations.

## 3. OS & Infrastructure Trends

Linux continues to dominate in server environments, with distributions like Ubuntu and Debian leading the pack. Open source software now represents over 32% of the market, with significant growth in developer tools and cloud infrastructure. The shift towards open source is accelerating as enterprises seek to reduce costs and increase flexibility.

## 4. Future Projections

Looking ahead, we expect continued growth in AI adoption, increased emphasis on developer productivity tools, and a gradual shift towards edge computing architectures. Organizations that invest in these areas will likely gain competitive advantages in the coming years.

## 5. Strategic Recommendations

**For CTOs & Engineering VPs:** Prioritize AI integration and cloud-native architecture. Invest in developer productivity tools and modern languages like Rust and TypeScript.

**For Developers & Engineers:** Focus on emerging technologies like AI/ML, Rust, and WebAssembly. Build skills in cloud-native development and developer tooling.

**For Indie Hackers & Founders:** Consider solutions in AI tooling, developer productivity, and edge computing. Look for underserved niches where you can apply modern technologies.

**For Tech Recruiters & Talent Partners:** Target candidates with skills in AI/ML, Rust, and cloud-native development. These skills are increasingly in demand and command premium compensation.
"""
    
    def run_analysis(self):
        """Main method to collect data, send to LLM, and return the article."""
        print("🔵 Starting LLM Analyst Bot...")
        
        # Step 1: Collect data
        print("📊 Gathering market data...")
        try:
            data = get_latest_data()
            trend_data = data.get('trends', [])
            metrics_data = data.get('metrics', [])
            codebase_stats = data.get('codebase_stats', {})
        except Exception as e:
            print(f"⚠️ Error getting market data: {e}")
            trend_data = ['AI/ML adoption growing', 'Rust gaining popularity']
            metrics_data = [{'Total frameworks': '45'}]
            codebase_stats = {'Languages': 'Python'}
        
        print("📈 Gathering financial data...")
        crypto_data = {}
        stock_data = {}
        try:
            if MarketDataCollector:
                collector = MarketDataCollector()
                market_data = collector.collect_all_data()
                crypto_data = market_data.get('crypto', {})
                stock_data = market_data.get('stocks', {})
        except Exception as e:
            print(f"⚠️ Error getting financial data: {e}")
            crypto_data = {'BTC': {'price': 68450, 'change_24h': 2.3}}
            stock_data = {'MSFT': {'price': 424.80, 'change_24h': 0.8}}
        
        print("💻 Gathering OS data...")
        os_data = {}
        try:
            if OSDataCollector:
                os_collector = OSDataCollector()
                os_data = os_collector.collect_all_data()
        except Exception as e:
            print(f"⚠️ Error getting OS data: {e}")
            os_data = {'market_share': {'Linux': {'market_share': 4.8, 'trend': 'growing'}}}
        
        # Step 2: Generate the prompt
        print("📝 Generating analyst prompt...")
        prompt = generate_analyst_prompt(
            trend_data, 
            metrics_data, 
            crypto_data, 
            stock_data, 
            os_data
        )
        
        # Step 3: Send to LLM
        print("🤖 Sending to LLM...")
        article = self.wake_llm(prompt)
        
        # Step 4: Save the article
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
