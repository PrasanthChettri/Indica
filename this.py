import requests
import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def fetch_with_requests(ticker):
    url = f'https://stocktwits.com/symbol/{ticker}'
    headers = {'User-Agent': 'Mozilla/5.0'}
    r = requests.get(url, headers=headers)
    # Attempt to find JSON endpoint (e.g. /streams/symbol/{ticker}.json)
    m = re.search(r'(/streams/symbol/' + re.escape(ticker) + r'.*?\.json)', r.text)
    if m:
        json_url = 'https://stocktwits.com' + m.group(1)
        resp = requests.get(json_url, headers=headers)
        return resp.json().get('messages', [])
    return None

def fetch_with_selenium(ticker):
    opts = Options()
    opts.add_argument("--headless")
    driver = webdriver.Chrome(options=opts)
    driver.get(f'https://stocktwits.com/symbol/{ticker}')
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()
    posts = []
    for twit in soup.select('div.stream-item'):
        txt = twit.get_text(strip=True)
        sentiment = None
        if 'Bullish' in txt:
            sentiment = 'Bullish'
        elif 'Bearish' in txt:
            sentiment = 'Bearish'
        posts.append({'text': txt, 'sentiment': sentiment})
    return posts

def scrape_stocktwits(ticker):
    messages = fetch_with_requests(ticker)
    if messages is None:
        print("JSON fetch failed; switching to Selenium...")
        return fetch_with_selenium(ticker)
    return [{'text': m.get('body'), 'sentiment': m.get('entities', {}).get('sentiment', {}).get('basic')} for m in messages]

if __name__ == "__main__":
    ticker = input("Enter StockTwits ticker (e.g. TATAMOTORS.NSE): ").strip().upper()
    messages = scrape_stocktwits(ticker)
    print(f"Found {len(messages)} messages for {ticker}")
    for msg in messages[:10]:
        print(f"[{msg['sentiment']}] {msg['text'][:100]}...")

