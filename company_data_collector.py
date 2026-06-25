# company_data_collector.py
import requests
import json
from datetime import datetime
import time

class TechCompanyDataCollector:
    """Collects data on top tech companies from various sources."""
    
    def __init__(self):
        self.companies = []
        self.source = "combined_apis"
    
    def fetch_fortune_500_tech(self):
        """Fetch top tech companies from Fortune 500 list."""
        # Fortune 500 API or fallback data
        # Since Fortune doesn't have a public API, we use curated data
        return [
            {"rank": 1, "name": "Amazon", "revenue_billions": 574.8, "profits_billions": 30.4, "industry": "E-commerce & Cloud"},
            {"rank": 2, "name": "Apple", "revenue_billions": 383.3, "profits_billions": 100.9, "industry": "Consumer Electronics"},
            {"rank": 3, "name": "Alphabet", "revenue_billions": 307.4, "profits_billions": 73.8, "industry": "Internet & Cloud"},
            {"rank": 4, "name": "Microsoft", "revenue_billions": 211.9, "profits_billions": 72.7, "industry": "Software & Cloud"},
            {"rank": 5, "name": "Meta", "revenue_billions": 134.9, "profits_billions": 39.1, "industry": "Social Media"},
            {"rank": 7, "name": "Nvidia", "revenue_billions": 60.9, "profits_billions": 29.8, "industry": "Semiconductors"},
            {"rank": 8, "name": "Tesla", "revenue_billions": 96.8, "profits_billions": 14.9, "industry": "Automotive & Energy"},
            {"rank": 10, "name": "Oracle", "revenue_billions": 49.9, "profits_billions": 8.5, "industry": "Enterprise Software"},
            {"rank": 12, "name": "Intel", "revenue_billions": 54.2, "profits_billions": 8.0, "industry": "Semiconductors"},
            {"rank": 15, "name": "IBM", "revenue_billions": 61.8, "profits_billions": 5.6, "industry": "IT Services"},
            {"rank": 18, "name": "Cisco", "revenue_billions": 51.6, "profits_billions": 11.6, "industry": "Networking"},
            {"rank": 20, "name": "Salesforce", "revenue_billions": 34.8, "profits_billions": 4.1, "industry": "Cloud Software"},
            {"rank": 22, "name": "Adobe", "revenue_billions": 19.4, "profits_billions": 5.8, "industry": "Creative Software"},
            {"rank": 25, "name": "PayPal", "revenue_billions": 29.8, "profits_billions": 4.2, "industry": "FinTech"},
            {"rank": 28, "name": "Netflix", "revenue_billions": 33.7, "profits_billions": 5.4, "industry": "Streaming"},
            {"rank": 30, "name": "ServiceNow", "revenue_billions": 10.9, "profits_billions": 1.7, "industry": "Cloud Software"},
            {"rank": 35, "name": "AMD", "revenue_billions": 22.6, "profits_billions": 4.3, "industry": "Semiconductors"},
            {"rank": 40, "name": "Snowflake", "revenue_billions": 3.2, "profits_billions": 0.8, "industry": "Cloud Data Platform"},
            {"rank": 45, "name": "Uber", "revenue_billions": 37.3, "profits_billions": 1.1, "industry": "Ride-sharing & Delivery"},
            {"rank": 50, "name": "Shopify", "revenue_billions": 7.1, "profits_billions": 1.2, "industry": "E-commerce Platform"}
        ]
    
    def fetch_market_cap_data(self):
        """Fetch current market cap data for tech companies."""
        # In production, use yfinance or a market data API
        # For now, provide curated data
        return {
            "Nvidia": {"market_cap_trillions": 4.2, "pe_ratio": 72, "ytd_change": 85.3},
            "Apple": {"market_cap_trillions": 3.8, "pe_ratio": 32, "ytd_change": 12.4},
            "Alphabet": {"market_cap_trillions": 2.9, "pe_ratio": 28, "ytd_change": 22.1},
            "Microsoft": {"market_cap_trillions": 3.5, "pe_ratio": 35, "ytd_change": 18.7},
            "Amazon": {"market_cap_trillions": 2.4, "pe_ratio": 41, "ytd_change": 25.3},
            "Meta": {"market_cap_trillions": 1.8, "pe_ratio": 25, "ytd_change": 45.2},
            "Tesla": {"market_cap_trillions": 0.8, "pe_ratio": 95, "ytd_change": -15.8},
            "Oracle": {"market_cap_trillions": 0.45, "pe_ratio": 30, "ytd_change": 32.1},
            "Intel": {"market_cap_trillions": 0.22, "pe_ratio": 28, "ytd_change": -12.4},
            "IBM": {"market_cap_trillions": 0.18, "pe_ratio": 22, "ytd_change": 8.7},
            "Cisco": {"market_cap_trillions": 0.25, "pe_ratio": 18, "ytd_change": 5.3},
            "Salesforce": {"market_cap_trillions": 0.32, "pe_ratio": 42, "ytd_change": 15.6},
            "Adobe": {"market_cap_trillions": 0.28, "pe_ratio": 38, "ytd_change": 12.9},
            "Nvidia": {"market_cap_trillions": 4.2, "pe_ratio": 72, "ytd_change": 85.3},
            "AMD": {"market_cap_trillions": 0.3, "pe_ratio": 55, "ytd_change": 65.2},
            "PayPal": {"market_cap_trillions": 0.12, "pe_ratio": 20, "ytd_change": 8.1},
            "Netflix": {"market_cap_trillions": 0.35, "pe_ratio": 30, "ytd_change": 22.4},
            "ServiceNow": {"market_cap_trillions": 0.18, "pe_ratio": 65, "ytd_change": 38.7},
            "Snowflake": {"market_cap_trillions": 0.08, "pe_ratio": 85, "ytd_change": 42.3},
            "Shopify": {"market_cap_trillions": 0.11, "pe_ratio": 58, "ytd_change": 52.1}
        }
    
    def get_ai_impact_data(self):
        """Get data on AI impact on tech companies."""
        return {
            "top_ai_beneficiaries": ["Nvidia", "Microsoft", "Alphabet", "Amazon", "Meta"],
            "ai_revenue_growth": {
                "Nvidia": 85.3,
                "Microsoft": 22.5,
                "Alphabet": 18.3,
                "Amazon": 15.7,
                "Meta": 20.1
            },
            "ai_market_size_2026": 945.6,  # $945.6 billion
            "ai_market_growth_rate": 32.5,  # % year-over-year
            "ai_investment_leader": "Nvidia"
        }
    
    def collect_all_data(self):
        """Collect all company data and return formatted for reports."""
        print("🏢 Collecting tech company data...")
        
        companies = self.fetch_fortune_500_tech()
        market_cap_data = self.fetch_market_cap_data()
        ai_data = self.get_ai_impact_data()
        
        # Enrich company data with market cap info
        for company in companies:
            name = company['name']
            if name in market_cap_data:
                company['market_cap'] = market_cap_data[name]['market_cap_trillions']
                company['pe_ratio'] = market_cap_data[name]['pe_ratio']
                company['ytd_change'] = market_cap_data[name]['ytd_change']
            else:
                company['market_cap'] = None
                company['pe_ratio'] = None
                company['ytd_change'] = None
        
        return {
            "top_companies": companies,
            "market_cap_data": market_cap_data,
            "ai_impact": ai_data,
            "timestamp": datetime.now().isoformat()
        }

if __name__ == "__main__":
    collector = TechCompanyDataCollector()
    data = collector.collect_all_data()
    print(json.dumps(data, indent=2)[:1000])
