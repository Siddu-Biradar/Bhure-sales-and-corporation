# ============================================
# Bhure Electrical - New Arrivals Manager
# ============================================
# Track and announce new product arrivals to customers

import json
import os
from datetime import datetime

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
PRODUCTS_FILE = os.path.join(DATA_DIR, 'products.json')

def ensure_data_dir():
    os.makedirs(DATA_DIR, exist_ok=True)

def load_products():
    """Load products database"""
    ensure_data_dir()
    if os.path.exists(PRODUCTS_FILE):
        with open(PRODUCTS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_products(products):
    """Save products database"""
    ensure_data_dir()
    with open(PRODUCTS_FILE, 'w', encoding='utf-8') as f:
        json.dump(products, f, indent=2, ensure_ascii=False)

def add_product(name, category, brand, price, mrp=None, description='', is_new_arrival=True):
    """Add a new product"""
    products = load_products()
    
    product = {
        'id': len(products) + 1,
        'name': name,
        'category': category,
        'brand': brand,
        'price': price,
        'mrp': mrp or price,
        'description': description,
        'is_new_arrival': is_new_arrival,
        'added_date': datetime.now().strftime('%Y-%m-%d'),
        'is_active': True
    }
    
    products.append(product)
    save_products(products)
    return True, f"Product '{name}' added! ID: {product['id']}"

def get_new_arrivals(limit=10):
    """Get recent new arrival products"""
    products = load_products()
    new_arrivals = [p for p in products if p.get('is_new_arrival', False) and p.get('is_active', True)]
    return sorted(new_arrivals, key=lambda x: x.get('added_date', ''), reverse=True)[:limit]

def get_products_by_category(category):
    """Get products by category"""
    products = load_products()
    return [p for p in products if p.get('category', '').lower() == category.lower() and p.get('is_active', True)]

def generate_new_arrival_message(products_list=None, customer_name="Customer", shop_name="Bhure Electrical"):
    """Generate WhatsApp message for new arrivals"""
    if products_list is None:
        products_list = get_new_arrivals(5)
    
    if not products_list:
        return None
    
    product_lines = []
    for p in products_list[:5]:
        discount = ''
        if p.get('mrp', 0) > p.get('price', 0):
            disc_pct = round((1 - p['price']/p['mrp']) * 100)
            discount = f" _(Save {disc_pct}%!)_"
        
        product_lines.append(
            f"▪️ *{p['name']}* ({p.get('brand', '')})\n"
            f"   ₹{p['price']:,}{discount}"
        )
    
    products_text = "\n\n".join(product_lines)
    
    message = f"""🆕✨ *NEW ARRIVALS at {shop_name}!* ✨🆕

Dear {customer_name} ji,

Check out what's *NEW* at our shop! 🛒

{products_text}

📍 Visit *{shop_name}* to see these products!
📞 Call/WhatsApp us for more details

_Limited stock available!_

~ Team {shop_name}"""
    
    return message

def generate_product_offer_message(product, discount_pct, customer_name="Customer", shop_name="Bhure Electrical"):
    """Generate offer message for a specific product"""
    offer_price = round(product['price'] * (1 - discount_pct/100))
    
    message = f"""🔥 *SPECIAL OFFER!* 🔥

Dear {customer_name} ji,

*{product['name']}* ({product.get('brand', '')})

~~₹{product['price']:,}~~ → *₹{offer_price:,}*
💰 Save ₹{product['price'] - offer_price:,} ({discount_pct}% OFF!)

📍 Available at *{shop_name}*
⏰ _Limited time offer!_

~ Team {shop_name}"""
    
    return message

def generate_category_showcase_message(category, customer_name="Customer", shop_name="Bhure Electrical"):
    """Generate category showcase message"""
    products = get_products_by_category(category)
    if not products:
        return None
    
    product_lines = []
    for p in products[:6]:
        product_lines.append(f"▪️ {p['name']} - ₹{p.get('price', 0):,}")
    
    products_text = "\n".join(product_lines)
    
    message = f"""🏪 *{category.upper()} Collection at {shop_name}!* 🏪

Dear {customer_name} ji,

Explore our *{category}* range:

{products_text}

...and many more in store!

📍 Visit *{shop_name}* today!
📞 Call us for pricing & availability

~ Team {shop_name}"""
    
    return message

# =============================================
# PREDEFINED PRODUCT CATEGORIES for Electrical Shop
# =============================================
PRODUCT_CATEGORIES = [
    "LED Lights",
    "Ceiling Fans",
    "Table Fans",
    "Exhaust Fans",
    "Switches & Sockets",
    "Wires & Cables",
    "MCBs & Distribution Boards",
    "Inverters & UPS",
    "Batteries",
    "Water Heaters / Geysers",
    "Room Heaters",
    "Coolers",
    "Stabilizers",
    "Decorative Lights",
    "Tube Lights",
    "Bulbs",
    "Extension Boards",
    "Modular Fittings",
    "Chandeliers",
    "Panel Lights",
    "Street Lights",
    "Solar Products",
    "Electrical Tools",
    "Motors & Pumps",
    "Doorbells",
    "CCTV & Security",
]

POPULAR_BRANDS = [
    "Havells", "Crompton", "Bajaj", "Orient", "Philips", "Syska",
    "Anchor", "Legrand", "Polycab", "Finolex", "Luminous", "V-Guard",
    "Wipro", "GM", "Usha", "KEI", "RR Kabel", "Schneider Electric",
    "Siemens", "ABB", "Panasonic", "Atomberg"
]
