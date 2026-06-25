# llm_analyst_prompt.py - Updated with company data
from company_data_collector import TechCompanyDataCollector

def generate_analyst_prompt(trend_data, metrics_data, crypto_data, stock_data, os_data, company_data=None):
    """Generate a comprehensive prompt for the LLM with company data included."""
    
    # If no company data provided, fetch it
    if company_data is None:
        collector = TechCompanyDataCollector()
        company_data = collector.collect_all_data()
    
    # Format all data
    trends_text = format_list(trend_data) if trend_data else "No trend data available."
    metrics_text = format_dict(metrics_data) if metrics_data else "No metrics data available."
    crypto_text = format_dict(crypto_data) if crypto_data else "No crypto data available."
    stock_text = format_dict(stock_data) if stock_data else "No stock data available."
    os_text = format_dict(os_data) if os_data else "No OS data available."
    
    # Format company data
    companies_text = format_companies(company_data.get('top_companies', []))
    ai_impact_text = format_ai_impact(company_data.get('ai_impact', {}))
    
    prompt = f"""You are a Senior Technology and Software Development Analyst with 20+ years of experience. Write a comprehensive tech analyst article based on the following data.

## 📊 REPORT DATA

### TOP SOFTWARE TRENDS
{trends_text}

### KEY METRICS
{metrics_text}

### CRYPTO MARKET DATA
{crypto_text}

### TECH STOCK PERFORMANCE
{stock_text}

### OPERATING SYSTEM POPULARITY
{os_text}

### TOP TECH COMPANIES (Ranked by Revenue)
{companies_text}

### AI IMPACT ON TECH INDUSTRY
{ai_impact_text}

## 📝 YOUR TASK

Write a detailed tech analyst article (800-1200 words) with these sections:

1. **Executive Summary** - High-level overview for CTOs and VPs
2. **Software Trends Deep Dive** - Detailed analysis of each trend
3. **Financial & Market Analysis** - Crypto, stocks, and company valuations
4. **Tech Company Landscape** - Analysis of the top tech companies, their performance, and market position
5. **AI Revolution Impact** - How AI is reshaping the tech industry
6. **OS & Infrastructure Trends** - Open source vs proprietary analysis
7. **Future Projections** - Where things are heading in 2-3 years
8. **Strategic Recommendations** - Actionable advice for:
   - CTOs & Engineering VPs
   - Developers & Software Engineers
   - Indie Hackers & Founders
   - Tech Recruiters & Talent Partners

## 🎯 KEY INSIGHTS TO INCLUDE

- The AI boom is adding over $30 trillion in shareholder value
- Nvidia leads the AI revolution with $4.2T market cap
- Amazon, Apple, Alphabet, Microsoft dominate by revenue
- Open source represents 32.5% of the software market
- Rust, TypeScript, and Edge Computing are key trends

Be data-driven, professional, and insightful. Use clear headings and bullet points for key takeaways.
"""
    return prompt

def format_companies(companies):
    """Format company list for the prompt."""
    if not companies:
        return "No company data available."
    
    lines = []
    for company in companies[:10]:  # Top 10
        line = f"  • Rank {company.get('rank', 'N/A')}: {company['name']} - Revenue: ${company.get('revenue_billions', 0)}B"
        if company.get('market_cap'):
            line += f", Market Cap: ${company['market_cap']}T"
        if company.get('ytd_change'):
            line += f", YTD: {company['ytd_change']}%"
        lines.append(line)
    
    return "\n".join(lines)

def format_ai_impact(ai_data):
    """Format AI impact data for the prompt."""
    if not ai_data:
        return "No AI impact data available."
    
    lines = [
        f"  • AI Market Size (2026): ${ai_data.get('ai_market_size_2026', 0)}B",
        f"  • AI Market Growth: {ai_data.get('ai_market_growth_rate', 0)}% YoY",
        f"  • Top AI Beneficiaries: {', '.join(ai_data.get('top_ai_beneficiaries', []))}",
        f"  • AI Investment Leader: {ai_data.get('ai_investment_leader', 'N/A')}"
    ]
    
    # Add AI revenue growth data
    growth_data = ai_data.get('ai_revenue_growth', {})
    if growth_data:
        lines.append("  • AI Revenue Growth:")
        for company, growth in growth_data.items():
            lines.append(f"    - {company}: {growth}%")
    
    return "\n".join(lines)

def format_list(items):
    if not items:
        return "No data available."
    if isinstance(items, list):
        return "\n".join([f"  {i+1}. {item}" for i, item in enumerate(items) if item])
    return str(items)

def format_dict(data):
    if not data:
        return "No data available."
    if isinstance(data, dict):
        lines = []
        for key, value in data.items():
            if isinstance(value, dict):
                lines.append(f"  • {key}: {value}")
            else:
                lines.append(f"  • {key}: {value}")
        return "\n".join(lines) if lines else "No data available."
    return str(data)
