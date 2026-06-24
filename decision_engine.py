def ping_google_indexing_api(url):
    """Ping Google's Indexing API to request crawling of new pages."""
    try:
        # Google's Indexing API endpoint (requires API key)
        # Note: This requires setting up a Google Cloud project and enabling the Indexing API
        # For now, we use the legacy sitemap ping as a fallback
        ping_url = f"https://www.google.com/ping?sitemap={url}"
        req = urllib.request.Request(ping_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            if response.status == 200:
                print(f"✅ Google indexing ping sent for: {url}")
                return True
            else:
                print(f"⚠️ Google ping returned: {response.status}")
                return False
    except Exception as e:
        print(f"⚠️ Google ping failed: {e}")
        return False

# Add to your make_decisions() function after creating new pages:
def make_decisions():
    # ... existing code ...
    
    # --- 7. Ping Google for new SEO pages ---
    posts_dir = "./posts"
    if os.path.exists(posts_dir):
        html_files = [f for f in os.listdir(posts_dir) if f.endswith('.html')]
        for file in html_files:
            url = f"https://manofmystery1981.github.io/global-software-trends/posts/{file}"
            ping_google_indexing_api(url)
