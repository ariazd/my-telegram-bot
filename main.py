import requests
import time

# =======================
# ⚙️ تنظیمات
TELEGRAM_TOKEN = "8426067776:AAEIsbHValh8nMxowqWzhVxuTIGj6YHr5pM"
CHAT_ID = "1627314745"
CHECK_INTERVAL = 300   # هر چند ثانیه یک بار بررسی (اینجا: 5 دقیقه)
TARGET_MULTIPLIER = 4  # یعنی 300 درصد سود (4 برابر شدن قیمت)
TOP_COINS = 30         # چندتا کوین با مارکت‌کپ پایین بررسی شوند
# =======================

# ذخیره قیمت اولیه کوین‌ها
initial_prices = {}

def send_telegram_message(message: str):
    """ارسال پیام به تلگرام"""
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": message}
    try:
        response = requests.post(url, data=data, timeout=30)
        if response.status_code != 200:
            print("⚠️ Telegram error:", response.text)
    except Exception as e:
        print("❌ Error sending message:", e)

def get_lowcap_coins():
    """گرفتن کوین‌های با مارکت‌کپ پایین"""
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "usd",
        "order": "market_cap_asc",
        "per_page": TOP_COINS,
        "page": 1,
        "price_change_percentage": "24h"
    }
    try:
        response = requests.get(url, params=params, timeout=30)
        return response.json()
    except Exception as e:
        print("❌ Error fetching coins:", e)
        return []

# 🚀 شروع کار
send_telegram_message("🤖 ربات تحلیل و سیگنال‌دهی کوین‌ها شروع به کار کرد!")

while True:
    try:
        lowcap_coins = get_lowcap_coins()

        if isinstance(lowcap_coins, list):
            for coin in lowcap_coins:
                coin_id = coin.get("id")
                coin_name = coin.get("name")
                coin_symbol = coin.get("symbol", "").upper()
                current_price = coin.get("current_price")
                market_cap = coin.get("market_cap")
                volume_24h = coin.get("total_volume")
                change_24h = coin.get("price_change_percentage_24h")

                if not coin_id or not current_price or not market_cap:
                    continue

                # اگر اولین بار دیدیم → تحلیل اولیه برای خرید
                if coin_id not in initial_prices:
                    if (market_cap and market_cap < 10_000_000 and 
                        volume_24h and volume_24h > (0.5 * market_cap) and 
                        change_24h and 0 < change_24h < 80):

                        initial_prices[coin_id] = current_price
                        send_telegram_message(
                            f"🟢 سیگنال خرید!\n"
                            f"{coin_name} ({coin_symbol})\n"
                            f"قیمت فعلی: {current_price} USD\n"
                            f"مارکت‌کپ: {market_cap} USD\n"
                            f"حجم 24h: {volume_24h} USD\n"
                            f"📊 تحلیل: احتمال رشد بالای 300٪"
                        )

                # بررسی شرط فروش (300٪ سود)
                else:
                    if current_price >= initial_prices[coin_id] * TARGET_MULTIPLIER:
                        send_telegram_message(
                            f"🚀 سیگنال فروش!\n"
                            f"{coin_name} ({coin_symbol})\n"
                            f"قیمت اولیه: {initial_prices[coin_id]} USD\n"
                            f"قیمت فعلی: {current_price} USD\n"
                            f"📈 رشد 300٪ رسید!"
                        )
                        del initial_prices[coin_id]

        else:
            print("⚠️ Unexpected response from API:", lowcap_coins)

    except Exception as e:
        print("❌ Error in loop:", e)

    time.sleep(CHECK_INTERVAL)
