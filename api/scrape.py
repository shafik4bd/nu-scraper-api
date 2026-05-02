from http.server import BaseHTTPRequestHandler
import requests
import urllib3
from bs4 import BeautifulSoup
import json
import os

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

SECRET_KEY = os.environ.get('SECRET_KEY', 'nu-scraper-secret-2026')
WP_URL     = os.environ.get('WP_URL', '')


def scrape_notices():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124',
        'Accept': 'text/html,application/xhtml+xml',
        'Accept-Language': 'bn-BD,bn;q=0.9,en;q=0.8',
        'Referer': 'https://www.nu.ac.bd/',
    }
    resp = requests.get(
        'https://www.nu.ac.bd/recent-news-notice.php',
        headers=headers, timeout=30, verify=False
    )
    resp.encoding = 'utf-8'

    soup  = BeautifulSoup(resp.text, 'html.parser')
    table = soup.find('table', {'id': 'myTable'})
    if not table:
        return [], 'Table #myTable not found'

    notices = []
    for row in table.find_all('tr')[1:]:
        cols = row.find_all('td')
        if len(cols) < 3:
            continue

        # col[0] = nu.ac.bd serial number
        try:
            serial = int(cols[0].get_text(strip=True))
        except:
            continue

        title = cols[1].get_text(separator=' ', strip=True)
        if not title or len(title) < 3:
            continue

        date = cols[2].get_text(strip=True)

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
            'serial':  serial,
            'title':   title,
            'date':    date,
            'pdf_url': pdf_url,
        })

    return notices, None


def push_to_wordpress(notices):
    if not WP_URL:
        return {'error': 'WP_URL not configured'}
    endpoint = WP_URL.rstrip('/') + '/wp-json/nu-scraper/v1/push'
    try:
        resp = requests.post(
            endpoint,
            json={'notices': notices, 'secret': SECRET_KEY},
            headers={'Content-Type': 'application/json'},
            timeout=60, verify=False
        )
        return resp.json()
    except Exception as e:
        return {'error': str(e)}


class handler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            from urllib.parse import urlparse, parse_qs
            params = parse_qs(urlparse(self.path).query)
            key = params.get('key', [''])[0]

            if key != SECRET_KEY:
                self._respond(401, {'error': 'Unauthorized'})
                return

            notices, err = scrape_notices()
            if err:
                self._respond(500, {'error': err, 'total': 0})
                return

            wp_result = {}
            if WP_URL and notices:
                wp_result = push_to_wordpress(notices)

            self._respond(200, {
                'success': True,
                'total':   len(notices),
                'preview': notices[:3],
                'wp_push': wp_result,
            })
        except Exception as e:
            self._respond(500, {'error': str(e)})

    def _respond(self, code, data):
        body = json.dumps(data, ensure_ascii=False).encode('utf-8')
        self.send_response(code)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-Length', len(body))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format, *args):
        pass
