# llm_analyst_prompt.py

def generate_analyst_prompt(trend_data, metrics_data, crypto_data, stock_data, os_data):
    """Generate a comprehensive prompt for the LLM to write a tech analyst article."""
    
    # Format the data
    trends_text = format_list(trend_data) if trend_data else "No trend data available."
    metrics_text = format_dict(metrics_data) if metrics_data else "No metrics data available."
    crypto_text = format_dict(crypto_data) if crypto_data else "No crypto data available."
    stock_text = format_dict(stock_data) if stock_data else "No stock data available."
    os_text = format_dict(os_data) if os_data else "No OS data available."
    
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

## 📝 YOUR TASK

Write a detailed tech analyst article (500-800 words) with these sections:

1. Executive Summary - high-level overview for CTOs and VPs
2. Software Trends Deep Dive - detailed analysis of each trend
3. Financial & Market Analysis - crypto and stock insights
4. OS & Infrastructure Trends - open source vs proprietary analysis
5. Future Projections - where things are heading in 2-3 years
6. Strategic Recommendations - actionable advice for CTOs, Developers, Indie Hackers, and Recruiters

Be data-driven, professional, and insightful. Use clear headings and bullet points for key takeaways.
"""
    return prompt

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
