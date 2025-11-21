# crypto-bot-ai
import requests
from telegram import Bot
from PIL import Image, ImageDraw, ImageFont
import datetime
import random
import os

TOKEN = "8525986458:AAGPAkcsf3a79d02imx1S6mslihewg65Hz4"
CHAT_ID = "-1001535659036"

bot = Bot(token=TOKEN)

# --- ФУНКЦІЯ ОТРИМАННЯ ЦІН ---
def get_prices():
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        "ids": "bitcoin,ethereum,solana,binancecoin,tether",
        "vs_currencies": "usd,uah"
    }
    r = requests.get(url, params=params).json()

    data = {
        "BTC": r["bitcoin"],
        "ETH": r["ethereum"],
        "SOL": r["solana"],
        "BNB": r["binancecoin"],
        "UAH": r["tether"]   # USDT → в UAH (1:1 до долара)
    }
    return data

# --- КАРТИНКА ---
def generate_image(data):
    img = Image.new("RGB", (1000, 600), (22, 22, 22))
    draw = ImageDraw.Draw(img)

    font_big = ImageFont.truetype("arial.ttf", 60)
    font_small = ImageFont.truetype("arial.ttf", 40)

    draw.text((50, 40), "Crypto Market Update", font=font_big, fill=(255, 255, 255))

    y = 160
    for coin, prices in data.items():
        text = f"{coin}:  ${prices['usd']}   |   ₴{prices['uah']}"
        draw.text((50, y), text, font=font_small, fill=(200, 200, 200))
        y += 70

    file = f"crypto_{random.randint(1000,9999)}.png"
    img.save(file)
    return file

# --- ТЕКСТОВИЙ ВИСНОВОК ---
def make_summary(data):
    btc = data["BTC"]["usd"]
    sol = data["SOL"]["usd"]

    if btc > 60000:
        mood = "ринок тримається впевнено."
    else:
        mood = "є легка напруга на графіках."

    summary = (
        f"📊 Ранковий огляд ринку\n"
        f"BTC зараз ${btc}. SOL біля ${sol}. Загалом {mood}"
    )

    return summary

# --- ГОЛОВНА ФУНКЦІЯ ---
def send_post():
    prices = get_prices()
    img = generate_image(prices)
    text = make_summary(prices)

    bot.send_photo(chat_id=CHAT_ID, photo=open(img, "rb"), caption=text)

    os.remove(img)


# --- АВТОЗАПУСК ---
send_post()
