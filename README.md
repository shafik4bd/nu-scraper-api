# nu-scraper-api
Nu Notice Feetcher API

পুরো Setup

# ধাপ — GitHub Repository বানান

github.com এ যান → New Repository → নাম দিন nu-scraper-api → Public → Create

# ধাপ ১ — GitHub এ Code Upload
vercel-scraper.zip extract করুন → GitHub এ nu-scraper-api repo তে এই ৩টা ফাইল upload করুন:

api/scrape.py
vercel.json
requirements.txt
ধাপ ২ — Vercel Deploy
vercel.com → Add New Project → GitHub repo select করুন → Environment Variables যোগ করুন:

# Variable ও	Value

SECRET_KEY হলো nu-scraper-secret-2026

WP_URL	হলো https://আপনার-সাইট.com

# → Deploy করুন

ধাপ ৩ — WordPress Plugin Install
nu-notice-scraper-final.zip আপলোড করে Activate করুন

# ধাপ ৪ — Test করুন
Browser এ যান:

https://আপনার-vercel-app.vercel.app/api/scrape?key=nu-scraper-secret-2026
কাজ করলে দেখাবে:

json
{"success": true, "total": 11309, ...}
এবং WordPress dashboard এ notices দেখা যাবে! ✅

Vercel Cron প্রতি ৫ মিনিটে automatically scrape করে WordPress এ push করবে।
