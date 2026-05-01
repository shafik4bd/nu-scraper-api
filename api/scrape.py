from http.server import BaseHTTPRequestHandler
import requests
from bs4 import BeautifulSoup
import json
import os
import hmac
import hashlib

SECRET_KEY = os.environ.get('SECRET_KEY', 'nu-scraper-secret-2026')
WP_URL     = os.environ.get('WP_URL', '')  # আপনার WordPress site URL

def scrape_notices():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124',
        'Accept': 'text/html,application/xhtml+xml',
        'Accept-Language': 'bn-BD,bn;q=0.9,en;q=0.8',
        'Referer': 'https://www.nu.ac.bd/',
    }

    resp = requests.get(
        'https://www.nu.ac.bd/recent-news-notice.php',
        headers=headers,
        timeout=30
    )
    resp.encoding = 'utf-8'

    soup = BeautifulSoup(resp.text, 'html.parser')
    table = soup.find('table', {'id': 'myTable'})

    if not table:
        return []

    notices = []
    rows = table.find_all('tr')[1:]  # header skip

    for row in rows:
        cols = row.find_all('td')
        if len(cols) < 3:
            continue

        # Title
        title = cols[1].get_text(separator=' ', strip=True)
        if not title or len(title) < 3:
            continue

        # Date
        date = cols[2].get_text(strip=True)

        # PDF link — last column or title column
        pdf_url = ''
        for col in reversed(cols):
            a = col.find('a', href=True)
            if a and '.pdf' in a['href'].lower():
                pdf_url = a['href']
                if not pdf_url.startswith('http'):
                    pdf_url = 'https://www.nu.ac.bd/' + pdf_url.lstrip('/')
                break

        if not pdf_url:
            continue

        notices.append({
            'title':    title,
            'date':     date,
            'pdf_url':  pdf_url,
        })

    return notices


def push_to_wordpress(notices):
    if not WP_URL:
        return {'error': 'WP_URL not set'}

    endpoint = WP_URL.rstrip('/') + '/wp-json/nu-scraper/v1/push'

    resp = requests.post(
        endpoint,
        json={'notices': notices, 'secret': SECRET_KEY},
        headers={'Content-Type': 'application/json'},
        timeout=30
    )
    return resp.json()


class handler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            # Secret key check
            from urllib.parse import urlparse, parse_qs
            params = parse_qs(urlparse(self.path).query)
            key = params.get('key', [''])[0]

            if key != SECRET_KEY:
                self.send_response(401)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'error': 'Unauthorized'}).encode())
                return

            # Scrape
            notices = scrape_notices()

            # Push to WordPress
            wp_result = {}
            if WP_URL and notices:
                wp_result = push_to_wordpress(notices)

            result = {
                'success': True,
                'total':   len(notices),
                'notices': notices[:5],  # preview only
                'wp_push': wp_result,
            }

            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(result, ensure_ascii=False).encode('utf-8'))

        except Exception as e:
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'error': str(e)}).encode())

    def log_message(self, format, *args):
        pass
