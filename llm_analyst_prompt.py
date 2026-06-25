# llm_analyst_prompt.py - Updated version
def format_companies(companies):
    """Format company list for the prompt with specific data points."""
    if not companies:
        return "No company data available."
    
    lines = []
    for company in companies[:15]:  # Top 15
        name = company.get('name', 'Unknown')
        revenue = company.get('revenue_billions', 0)
        market_cap = company.get('market_cap', 0)
        ytd_change = company.get('ytd_change', 0)
        pe_ratio = company.get('pe_ratio', 0)
        industry = company.get('industry', 'Unknown')
        
        line = f"  • {name}: ${revenue}B revenue"
        if market_cap:
            line += f", ${market_cap}T market cap"
        if ytd_change:
            line += f", {ytd_change}% YTD change"
        if pe_ratio:
            line += f", P/E: {pe_ratio}"
        line += f" ({industry})"
        lines.append(line)
    
    return "\n".join(lines)

def generate_analyst_prompt(trend_data, metrics_data, crypto_data, stock_data, os_data, company_data=None):
    """Generate a comprehensive prompt for the LLM with specific data points."""
    
    if company_data is None:
        from company_data_collector import TechCompanyDataCollector
        collector = TechCompanyDataCollector()
        company_data = collector.collect_all_data()
    
    # Format data with specific numbers
    trends_text = format_trends_with_data(trend_data)
    metrics_text = format_metrics_with_data(metrics_data)
    crypto_text = format_crypto_with_data(crypto_data)
    stock_text = format_stocks_with_data(stock_data)
    os_text = format_os_with_data(os_data)
    companies_text = format_companies(company_data.get('top_companies', []))
    ai_impact_text = format_ai_impact(company_data.get('ai_impact', {}))
    
    prompt = f"""You are a Senior Technology and Software Development Analyst with 20+ years of experience. Write a comprehensive, data-driven tech analyst article based on the following REAL market data. Be specific, use the actual numbers provided, and avoid generic statements.

## 📊 REAL MARKET DATA (USE THESE SPECIFIC NUMBERS)

### TOP SOFTWARE TRENDS (2026)
{trends_text}

### KEY METRICS
{metrics_text}

### CRYPTO MARKET DATA (Current)
{crypto_text}

### TECH STOCK PERFORMANCE (Current)
{stock_text}

### OPERATING SYSTEM POPULARITY
{os_text}

### TOP TECH COMPANIES
{companies_text}

### AI IMPACT ON TECH INDUSTRY
{ai_impact_text}

## 📝 YOUR TASK

Write a detailed, data-driven tech analyst article (1000-1500 words) with these sections:

1. **Executive Summary** - High-level overview using specific data points
2. **Software Trends Deep Dive** - Analyze each trend with the actual data
3. **Financial & Market Analysis** - Use the crypto and stock data provided
4. **Tech Company Landscape** - Discuss the top companies using their actual revenue, market cap, and performance data
5. **AI Revolution Impact** - Use the AI impact data provided
6. **Future Projections** - Based on the data, project where things are heading
7. **Strategic Recommendations** - Actionable advice for:
   - CTOs & Engineering VPs
   - Developers & Software Engineers
   - Indie Hackers & Founders
   - Tech Recruiters & Talent Partners

## 🎯 CRITICAL REQUIREMENTS

- **USE THE SPECIFIC NUMBERS** provided in the data above
- **CITE REAL DATA** - don't make up statistics
- **BE SPECIFIC** - mention actual companies, trends, and metrics
- **CURRENT YEAR IS 2026** - don't reference outdated projections
- **PROFESSIONAL TONE** - like a McKinsey or Stratechery report
- **STRUCTURED FORMAT** - use clear headings and bullet points

Begin your analysis now.
"""
    return prompt

def format_trends_with_data(trends):
    """Format trends with specific data points."""
    if not trends:
        return "No trend data available."
    return "\n".join([f"  • {trend}" for trend in trends])

def format_metrics_with_data(metrics):
    """Format metrics with specific values."""
    if not metrics:
        return "No metrics data available."
    lines = []
    for metric in metrics:
        if isinstance(metric, dict):
            for key, value in metric.items():
                lines.append(f"  • {key}: {value}")
        else:
            lines.append(f"  • {metric}")
    return "\n".join(lines)

def format_crypto_with_data(crypto):
    """Format crypto data with specific prices."""
    if not crypto:
        return "No crypto data available."
    lines = []
    for coin, data in crypto.items():
        price = data.get('price', 0)
        change = data.get('change_24h', 0)
        lines.append(f"  • {coin}: ${price:.2f} (24h: {change:+.1f}%)")
    return "\n".join(lines)

def format_stocks_with_data(stocks):
    """Format stock data with specific prices."""
    if not stocks:
        return "No stock data available."
    lines = []
    for symbol, data in stocks.items():
        price = data.get('price', 0)
        change = data.get('change_24h', 0)
        lines.append(f"  • {symbol}: ${price:.2f} (24h: {change:+.1f}%)")
    return "\n".join(lines)

def format_os_with_data(os_data):
    """Format OS data with specific market shares."""
    if not os_data:
        return "No OS data available."
    lines = []
    market_share = os_data.get('market_share', {})
    for os_name, data in market_share.items():
        share = data.get('market_share', 0)
        trend = data.get('trend', 'stable')
        category = data.get('category', 'Unknown')
        lines.append(f"  • {os_name}: {share}% market share ({trend}, {category})")
    return "\n".join(lines)

def format_ai_impact(ai_data):
    """Format AI impact data with specific numbers."""
    if not ai_data:
        return "No AI impact data available."
    
    lines = [
        f"  • AI Market Size (2026): ${ai_data.get('ai_market_size_2026', 0)}B",
        f"  • AI Market Growth: {ai_data.get('ai_market_growth_rate', 0)}% YoY",
        f"  • Top AI Beneficiaries: {', '.join(ai_data.get('top_ai_beneficiaries', []))}",
        f"  • AI Investment Leader: {ai_data.get('ai_investment_leader', 'N/A')}"
    ]
    
    growth_data = ai_data.get('ai_revenue_growth', {})
    if growth_data:
        lines.append("  • AI Revenue Growth:")
        for company, growth in growth_data.items():
            lines.append(f"    - {company}: {growth}%")
    
    return "\n".join(lines)

def format_top_100_companies(companies):
    """Format the top 100 companies with key metrics."""
    if not companies:
        return "No company data available."
    
    lines = []
    for company in companies[:100]:
        name = company.get('name', 'Unknown')
        rank = company.get('rank', 0)
        revenue = company.get('revenue_billions', 0)
        market_cap = company.get('market_cap_trillions', 0)
        ytd_change = company.get('ytd_change', 0)
        industry = company.get('industry', 'Unknown')
        trending = company.get('trending', '')
        
        line = f"  #{rank}. {name}: ${revenue}B revenue"
        if market_cap:
            line += f", ${market_cap}T market cap"
        if ytd_change:
            line += f", {ytd_change}% YTD"
        if trending:
            line += f" (Trending: {trending})"
        lines.append(line)
    
    return "\n".join(lines)

def format_trending_companies(companies):
    """Format the top 10 trending companies."""
    if not companies:
        return "No trending company data available."
    
    lines = ["**Top 10 Trending Tech Companies (by YTD Growth):**"]
    for company in companies[:10]:
        name = company.get('name', 'Unknown')
        ytd_change = company.get('ytd_change', 0)
        industry = company.get('industry', 'Unknown')
        lines.append(f"  • {name}: {ytd_change}% YTD ({industry})")
    
    return "\n".join(lines)

def format_cutting_edge_trends(trends):
    """Format cutting-edge software trends."""
    if not trends:
        return "No trend data available."
    
    lines = ["**Cutting-Edge Software Trends:**"]
    for trend in trends:
        name = trend.get('trend', 'Unknown')
        description = trend.get('description', '')
        adoption = trend.get('adoption_rate', 0)
        players = ', '.join(trend.get('key_players', []))
        lines.append(f"  • {name}: {description} (Adoption: {adoption}%, Key Players: {players})")
    
    return "\n".join(lines)
