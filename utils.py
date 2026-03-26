from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

def get_page_content(url):
    """
    I used Playwright because many modern sites use JavaScript.
    A simple 'requests' call would miss a lot of technologies.
    """
    if not url.startswith('http'):
        url = "https://" + url

    with sync_playwright() as p:
        try:
            # Launching chromium in headless mode (no window pops up)
            browser = p.chromium.launch(headless=True)
            # Setting a real user agent to avoid being blocked immediately
            context = browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
            )
            page = context.new_page()
            
            # Waiting for the page to load properly
            response = page.goto(url, timeout=30000, wait_until='load')

            if response:
                html = page.content()
                headers = response.headers
                browser.close()
                return {"html": html, "headers": headers}
            
            browser.close()
            return None
        except Exception as e:
            # If the site is down or times out, we just print a message
            print(f"Skipping {url} because: {e}")
            return None

def check_for_techs(html_content, headers, tech_list):
    """
    This function compares the website data with our JSON rules.
    It checks HTML content, meta tags, and headers.
    """
    found = []
    if not html_content:
        return []
    
    soup = BeautifulSoup(html_content, 'html.parser')
    # Converting headers to lowercase for easier matching
    low_headers = {k.lower(): v.lower() for k, v in headers.items()}

    for tech in tech_list:
        name = tech['name']
        proof = None

        # Look for text patterns in the HTML
        if "html_patterns" in tech:
            for pattern in tech['html_patterns']:
                if pattern.lower() in html_content.lower():
                    proof = f"Found pattern: '{pattern}' in HTML source"
                    break

        # Look for specific Meta Tags (very common for CMS like WordPress)
        if not proof and "meta_tags" in tech:
            for m_name, m_val in tech['meta_tags'].items():
                meta = soup.find("meta", attrs={"name": m_name}) or \
                       soup.find("meta", attrs={"property": m_name})
                if meta and m_val.lower() in meta.get("content", "").lower():
                    proof = f"Meta tag '{m_name}' indicates '{m_val}'"
                    break

        # Look in the HTTP Response Headers
        if not proof and "headers" in tech:
            for h_rule in tech['headers']:
                if ":" in h_rule:
                    h_key, h_val = h_rule.split(":", 1)
                    h_key, h_val = h_key.strip().lower(), h_val.strip().lower()
                    if h_val in low_headers.get(h_key, ""):
                        proof = f"HTTP header '{h_key}' indicates '{h_val}'"
                        break

        if proof:
            found.append({
                "technology": name, 
                "proof": proof
            })

    return found
    