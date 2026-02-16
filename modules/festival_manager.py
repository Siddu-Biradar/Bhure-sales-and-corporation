# ============================================
# Bhure Electrical - Festival & Event Manager
# ============================================
# Auto-sends festival wishes, birthday greetings, seasonal offers

import json
import os
from datetime import datetime, timedelta

FESTIVALS_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'festivals.json')

# =============================================
# INDIAN FESTIVALS & EVENTS for 2026
# (Update this every year or add more!)
# =============================================
FESTIVALS_2026 = [
    # === MAJOR FESTIVALS ===
    {"date": "2026-01-14", "name": "Makar Sankranti", "type": "festival", "emoji": "🪁"},
    {"date": "2026-01-26", "name": "Republic Day", "type": "national", "emoji": "🇮🇳"},
    {"date": "2026-03-10", "name": "Maha Shivratri", "type": "festival", "emoji": "🙏"},
    {"date": "2026-03-17", "name": "Holi", "type": "festival", "emoji": "🎨"},
    {"date": "2026-03-31", "name": "Ugadi / Gudi Padwa", "type": "festival", "emoji": "🌺"},
    {"date": "2026-04-02", "name": "Ram Navami", "type": "festival", "emoji": "🙏"},
    {"date": "2026-04-14", "name": "Baisakhi", "type": "festival", "emoji": "🌾"},
    {"date": "2026-05-10", "name": "Mother's Day", "type": "special_day", "emoji": "❤️"},
    {"date": "2026-05-12", "name": "Buddha Purnima", "type": "festival", "emoji": "🙏"},
    {"date": "2026-06-21", "name": "Father's Day", "type": "special_day", "emoji": "👨‍👧"},
    {"date": "2026-07-07", "name": "Rath Yatra", "type": "festival", "emoji": "🛕"},
    {"date": "2026-08-04", "name": "Raksha Bandhan", "type": "festival", "emoji": "🎀"},
    {"date": "2026-08-11", "name": "Janmashtami", "type": "festival", "emoji": "🦚"},
    {"date": "2026-08-15", "name": "Independence Day", "type": "national", "emoji": "🇮🇳"},
    {"date": "2026-08-27", "name": "Ganesh Chaturthi", "type": "festival", "emoji": "🐘"},
    {"date": "2026-09-05", "name": "Teachers' Day", "type": "special_day", "emoji": "📚"},
    {"date": "2026-10-02", "name": "Gandhi Jayanti", "type": "national", "emoji": "🕊️"},
    {"date": "2026-10-02", "name": "Navratri Begins", "type": "festival", "emoji": "🪔"},
    {"date": "2026-10-11", "name": "Dussehra / Vijayadashami", "type": "festival", "emoji": "🏹"},
    {"date": "2026-10-20", "name": "Karwa Chauth", "type": "festival", "emoji": "🌙"},
    {"date": "2026-10-29", "name": "Dhanteras", "type": "festival", "emoji": "💰"},
    {"date": "2026-10-31", "name": "Diwali", "type": "festival", "emoji": "🪔"},
    {"date": "2026-11-01", "name": "Govardhan Puja", "type": "festival", "emoji": "🙏"},
    {"date": "2026-11-02", "name": "Bhai Dooj", "type": "festival", "emoji": "👫"},
    {"date": "2026-11-14", "name": "Children's Day", "type": "special_day", "emoji": "👧"},
    {"date": "2026-11-24", "name": "Guru Nanak Jayanti", "type": "festival", "emoji": "🙏"},
    {"date": "2026-12-25", "name": "Christmas", "type": "festival", "emoji": "🎄"},
    {"date": "2026-12-31", "name": "New Year's Eve", "type": "special_day", "emoji": "🎉"},
    {"date": "2027-01-01", "name": "New Year 2027", "type": "special_day", "emoji": "🎊"},
    
    # === SEASONAL / SHOPPING EVENTS ===
    {"date": "2026-01-15", "name": "Winter Sale Season", "type": "sale", "emoji": "❄️"},
    {"date": "2026-04-01", "name": "Summer Season Sale", "type": "sale", "emoji": "☀️"},
    {"date": "2026-06-15", "name": "Monsoon Season Sale", "type": "sale", "emoji": "🌧️"},
    {"date": "2026-10-25", "name": "Diwali Mega Sale", "type": "sale", "emoji": "🛒"},
]

def load_festivals():
    """Load festivals from JSON file or use defaults"""
    os.makedirs(os.path.dirname(FESTIVALS_FILE), exist_ok=True)
    if os.path.exists(FESTIVALS_FILE):
        with open(FESTIVALS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    else:
        save_festivals(FESTIVALS_2026)
        return FESTIVALS_2026

def save_festivals(festivals):
    """Save festivals to JSON"""
    os.makedirs(os.path.dirname(FESTIVALS_FILE), exist_ok=True)
    with open(FESTIVALS_FILE, 'w', encoding='utf-8') as f:
        json.dump(festivals, f, indent=2, ensure_ascii=False)

def add_festival(date, name, festival_type='festival', emoji='🎉'):
    """Add a custom festival/event"""
    festivals = load_festivals()
    festivals.append({
        "date": date,
        "name": name,
        "type": festival_type,
        "emoji": emoji
    })
    festivals.sort(key=lambda x: x['date'])
    save_festivals(festivals)
    return True, f"Added {name} on {date}"

def get_today_festivals():
    """Get festivals for today"""
    today = datetime.now().strftime('%Y-%m-%d')
    festivals = load_festivals()
    return [f for f in festivals if f['date'] == today]

def get_upcoming_festivals(days=7):
    """Get festivals in the next N days"""
    today = datetime.now()
    end_date = today + timedelta(days=days)
    festivals = load_festivals()
    
    upcoming = []
    for f in festivals:
        try:
            f_date = datetime.strptime(f['date'], '%Y-%m-%d')
            if today <= f_date <= end_date:
                days_until = (f_date - today).days
                f['days_until'] = days_until
                upcoming.append(f)
        except:
            pass
    
    return sorted(upcoming, key=lambda x: x['date'])

def get_festival_message(festival_name, customer_name, shop_name="Bhure Electrical"):
    """Generate a festival-specific greeting message"""
    
    messages = {
        "Diwali": f"""🪔✨ *Happy Diwali!* ✨🪔

Dear {customer_name} ji,

Wishing you and your family a very *Happy Diwali!* 🎆

May this festival of lights bring brightness, happiness, and prosperity to your home!

🏪 *{shop_name}* wishes you:
✨ Dhanteras ka dhan
🪔 Diwali ki roshni  
🎆 Naye saal ki khushiyan

_Light up your home with the best electrical items from {shop_name}!_

🎁 *Special Diwali Offers Available!*
Visit us today for amazing deals on:
💡 LED Lights & Decorations
⚡ Fans, Heaters & Appliances
🔌 Switches, Wires & Fittings

Thank you for being our valued customer! 🙏
~ Team {shop_name}""",
        
        "Holi": f"""🎨🌈 *Happy Holi!* 🌈🎨

Dear {customer_name} ji,

*{shop_name}* wishes you a colorful and joyful Holi! 🎉

May your life be as colorful and bright as the festival of colors!

Rang barse! 🎨
~ Team {shop_name}""",

        "Makar Sankranti": f"""🪁☀️ *Happy Makar Sankranti!* ☀️🪁

Dear {customer_name} ji,

Wishing you a very *Happy Makar Sankranti!*

May the sun bring warmth, joy, and new energy into your life!

Tilgul ghya, god god bola! 🍫

~ Team {shop_name}""",

        "Republic Day": f"""🇮🇳 *Happy Republic Day!* 🇮🇳

Dear {customer_name} ji,

Wishing you a proud *Republic Day!* 🎖️

Jai Hind! 🇮🇳

~ Team {shop_name}""",

        "Independence Day": f"""🇮🇳 *Happy Independence Day!* 🇮🇳

Dear {customer_name} ji,

*{shop_name}* wishes you a very *Happy Independence Day!*

Vande Mataram! 🇮🇳

~ Team {shop_name}""",

        "Raksha Bandhan": f"""🎀 *Happy Raksha Bandhan!* 🎀

Dear {customer_name} ji,

Wishing you a wonderful *Raksha Bandhan* filled with love and togetherness!

🎁 *Gift your sister the best from {shop_name}!*

~ Team {shop_name}""",

        "Ganesh Chaturthi": f"""🐘🙏 *Ganpati Bappa Morya!* 🙏🐘

Dear {customer_name} ji,

Wishing you a blessed *Ganesh Chaturthi!*

May Lord Ganesha bless you with wisdom and prosperity!

🪔 *Decoration lights & electrical items available at special prices!*

~ Team {shop_name}""",

        "Navratri Begins": f"""🪔 *Happy Navratri!* 🪔

Dear {customer_name} ji,

*Jai Mata Di!* 🙏

Wishing you 9 nights of devotion, dance and celebration!

🪔 *Special Navratri collection of lights available at {shop_name}!*

~ Team {shop_name}""",

        "Dussehra / Vijayadashami": f"""🏹 *Happy Dussehra!* 🏹

Dear {customer_name} ji,

Wishing you a victorious *Vijayadashami!*

May good always triumph over evil!

~ Team {shop_name}""",

        "Dhanteras": f"""💰✨ *Happy Dhanteras!* ✨💰

Dear {customer_name} ji,

Wishing you a prosperous *Dhanteras!*

🛒 *It's auspicious to buy electrical items today!*
Visit *{shop_name}* for special Dhanteras offers!

💡 LED Lights ⚡ Fans 🔌 Appliances

~ Team {shop_name}""",

        "Christmas": f"""🎄 *Merry Christmas!* 🎄

Dear {customer_name} ji,

Wishing you a *Merry Christmas* and happy holidays! 🎅

🎁 *Christmas Special Offers at {shop_name}!*

~ Team {shop_name}""",

        "New Year's Eve": f"""🎉 *Happy New Year!* 🎊

Dear {customer_name} ji,

Wishing you a very *Happy New Year 2027!* 🎆

May the coming year bring you health, happiness, and prosperity!

Thank you for being a valued customer of *{shop_name}!*
We look forward to serving you in the new year!

🎊 *New Year Special Offers Coming Soon!*

~ Team {shop_name}""",

        "Mother's Day": f"""❤️ *Happy Mother's Day!* ❤️

Dear {customer_name} ji,

Wishing all mothers a very Happy Mother's Day!

🎁 *Gift your mother something special from {shop_name}!*

~ Team {shop_name}""",

        "Father's Day": f"""👨‍👧 *Happy Father's Day!* 👨‍👧

Dear {customer_name} ji,

Wishing all fathers a very Happy Father's Day!

🎁 *Gift your father something special from {shop_name}!*

~ Team {shop_name}""",
    }
    
    # Default message for festivals not in the dictionary
    default_msg = f"""🎉 *Happy {festival_name}!* 🎉

Dear {customer_name} ji,

*{shop_name}* wishes you a very *Happy {festival_name}!*

May this occasion bring joy and happiness to you and your family! 🙏

Thank you for being our valued customer!
~ Team {shop_name}"""
    
    return messages.get(festival_name, default_msg)

def get_birthday_message(customer_name, shop_name="Bhure Electrical"):
    """Generate birthday greeting"""
    return f"""🎂🎉 *Happy Birthday, {customer_name} ji!* 🎉🎂

Wishing you a wonderful birthday filled with joy and happiness!

🎁 *Special Birthday Gift from {shop_name}!*
Show this message at our shop to get a *special 10% discount* on your next purchase!
_(Valid for 7 days)_

Thank you for being part of the {shop_name} family! 🙏
~ Team {shop_name}"""

def get_anniversary_message(customer_name, shop_name="Bhure Electrical"):
    """Generate anniversary greeting"""
    return f"""💍✨ *Happy Anniversary, {customer_name} ji!* ✨💍

Wishing you a very Happy Anniversary!

May your love grow brighter every year! 💕

🎁 *Anniversary Special* - Visit {shop_name} for special offers!

~ Team {shop_name}"""

def get_seasonal_sale_message(season, customer_name, shop_name="Bhure Electrical"):
    """Generate seasonal sale messages"""
    
    messages = {
        "Winter Sale Season": f"""❄️ *WINTER SALE at {shop_name}!* ❄️

Dear {customer_name} ji,

Beat the cold with our *Winter Special Offers!*

🔥 Room Heaters - Starting ₹999
💡 LED Lights - Flat 20% OFF
⚡ Geysers & Water Heaters - Best Prices!
🔌 All Electrical Fittings - Special Discount

📍 Visit *{shop_name}* today!
_Limited stock, limited period offer!_

~ Team {shop_name}""",

        "Summer Season Sale": f"""☀️ *SUMMER MEGA SALE at {shop_name}!* ☀️

Dear {customer_name} ji,

Beat the heat with our *Summer Special Offers!*

🌀 Ceiling Fans - Starting ₹1,299
❄️ Coolers - Flat 15% OFF
💡 LED Lights - Buy 3 Get 1 FREE
⚡ Stabilizers - Special Prices!

📍 Visit *{shop_name}* today!
_Don't miss out!_

~ Team {shop_name}""",

        "Monsoon Season Sale": f"""🌧️ *MONSOON SALE at {shop_name}!* 🌧️

Dear {customer_name} ji,

Stay safe this monsoon with our *Special Offers!*

⚡ MCBs & Safety Switches - 25% OFF
🔌 Waterproof Fittings - Special Price
💡 Inverters & UPS - Best Deals!
🔋 Batteries - Flat Discount

📍 Visit *{shop_name}* today!

~ Team {shop_name}""",

        "Diwali Mega Sale": f"""🪔🛒 *DIWALI MEGA SALE at {shop_name}!* 🛒🪔

Dear {customer_name} ji,

🎉 *Our BIGGEST SALE of the year is HERE!* 🎉

💡 Decorative LED Lights - Flat 30% OFF
🌟 Fancy Lights & Jhalar - Starting ₹99
⚡ Fans & Appliances - Up to 40% OFF
🔌 Switches & Fittings - Special Diwali Price
🔋 Inverters - Exchange Offer Available!

📍 Visit *{shop_name}* today!
_Offer valid till Diwali!_

🪔 Light up your Diwali with {shop_name}! 🪔

~ Team {shop_name}""",
    }
    
    return messages.get(season, f"🎉 *Special Sale at {shop_name}!* Visit us for amazing deals! ~ Team {shop_name}")
