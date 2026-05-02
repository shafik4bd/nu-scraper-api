# 🚀 nu-scraper-api: Nu Notice Fetcher API

এখানে আপনার **NU Notice Scraper**-এর সম্পূর্ণ সেটআপ গাইড দেওয়া হলো। ধাপগুলো সাবধানে অনুসরণ করুন।

---

## 📂 ধাপ ০: GitHub Repository তৈরি করুন
1. [github.com](https://github.com)-এ যান।
2. **New Repository**-তে ক্লিক করুন।
3. নাম দিন: `nu-scraper-api`
4. **Public** সিলেক্ট করে **Create Repository**-তে ক্লিক করুন।

## ☁️ ধাপ ১: GitHub-এ Code Upload করুন
আপনার পিসিতে থাকা `vercel-scraper.zip` ফাইলটি আনজিপ (extract) করুন। এরপর নিচের ৩টি ফাইল আপনার GitHub রিপোজিটরিতে আপলোড করুন:

```text
api/scrape.py
vercel.json
requirements.txt
```
# 🚀 ধাপ ২: Vercel-এ Deploy করুন

`vercel.com`-এ যান এবং `Add New Project`-এ ক্লিক করুন।আপনার `GitHub` রিপোজিটরি `(nu-scraper-api)` সিলেক্ট করে Import করুন।`Environment Variables` অপশনে গিয়ে নিচের তথ্যগুলো যোগ করুন:
```
Variable Name,Value
SECRET_KEY, nu-scraper-secret-2026
WP_URL, https://আপনার-সাইট.com
```

# 🔌 ধাপ ৪ — wp plugin install করুন
ফাইলের মধ্যে থাকা `nu notice scrapper.zip` ফাইল ডাউনলোড করুন এবং ওয়ার্ডপ্রেসে ইন্সটল করুন

# 🧪 ধাপ ৫ — Test করুন 
Browser এ যান:

https://আপনার-vercel-app.vercel.app/api/scrape?key=nu-scraper-secret-2026
কাজ করলে দেখাবে:
```json
{"success": true, "total": 11309, ...}
```
এবং WordPress dashboard এ notices দেখা যাবে! ✅


> [!NOTE]
> **অটোমেশন:** WordPress Cron সেটআপ করা আছে, যা প্রতি ৫ মিনিট পরপর স্বয়ংক্রিয়ভাবে নোটিশগুলো স্ক্র্যাপ করে আপনার সাইটে পুশ করবে। এই api সম্পূর্ণ ওয়ার্ডপ্রেস সাইটের জন্য। যতবার এপিআই লিঙ্কে প্রবেশ করবেন ততবার নোটিশগুলো আপনার ওয়ার্ডপ্রেসের REST API এর মাধ্যমে প্লাগিনের ড্যাসবোডে চলে যাবে।  পিএইচপি বা লারাভেল সাইটের জন্য claude code দিয়ে ডিজাইন করে নিবেন।
