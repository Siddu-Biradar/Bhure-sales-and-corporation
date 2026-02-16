# ============================================
# Bhure Electrical - Quick Message Templates
# ============================================
# Ready-to-use message templates for various engagement scenarios

SHOP_NAME = "Bhure Electrical"

# =============================================
# 1. WELCOME MESSAGE (for new customers)
# =============================================
def welcome_message(customer_name):
    return f"""🏪 *Welcome to {SHOP_NAME}!* 🏪

Dear {customer_name} ji,

Thank you for visiting *{SHOP_NAME}!* 🙏

We are your one-stop shop for all electrical needs:
💡 LED Lights & Bulbs
⚡ Fans (Ceiling, Table, Exhaust)
🔌 Switches, Sockets & Fittings
🔋 Inverters, UPS & Batteries
🔧 Wires, Cables & MCBs
🏠 Home Appliances

✅ *Why choose us?*
✔️ Branded products at best prices
✔️ Expert advice & guidance
✔️ After-sales support
✔️ Home delivery available

Save this number for:
📞 Quick orders
📋 Product enquiries
🎉 Festival offers & deals

We look forward to serving you! 🙏
~ Team {SHOP_NAME}"""


# =============================================
# 2. SHOP TIMING / INFO MESSAGE
# =============================================
def shop_info_message():
    return f"""🏪 *{SHOP_NAME} - Shop Details* 🏪

📍 *Address:* [Your Address Here]
📞 *Phone:* [Your Number]
⏰ *Timings:* 9:00 AM - 9:00 PM (Mon-Sat)
   Sunday: 10:00 AM - 2:00 PM

💳 *Payment Modes:*
✔️ Cash
✔️ UPI (Google Pay / PhonePe / Paytm)  
✔️ Credit/Debit Cards
✔️ EMI Available on select items

🚗 *Home Delivery Available!*

Follow us for latest offers & updates! 📱
~ Team {SHOP_NAME}"""


# =============================================
# 3. GENERIC OFFER MESSAGE
# =============================================
def offer_message(customer_name, offer_text, validity="Limited Period"):
    return f"""🔥 *SPECIAL OFFER at {SHOP_NAME}!* 🔥

Dear {customer_name} ji,

{offer_text}

📍 Visit *{SHOP_NAME}* today!
⏰ Offer valid: {validity}

_*Terms & conditions apply_

~ Team {SHOP_NAME}"""


# =============================================
# 4. PRODUCT ENQUIRY FOLLOW-UP
# =============================================
def enquiry_followup(customer_name, product_name):
    return f"""👋 *Following up on your enquiry!*

Dear {customer_name} ji,

Thank you for your enquiry about *{product_name}* at {SHOP_NAME}.

✅ The product is *available* at our shop!

Would you like to:
1️⃣ Visit the shop to see it
2️⃣ Get it delivered to your address
3️⃣ Know more about other options

Just reply to this message! 📱

~ Team {SHOP_NAME}"""


# =============================================
# 5. OUT OF STOCK → BACK IN STOCK
# =============================================
def back_in_stock(customer_name, product_name, price=None):
    price_text = f"\n💰 Price: ₹{price:,}" if price else ""
    return f"""🔔 *Back in Stock!* 🔔

Dear {customer_name} ji,

Great news! *{product_name}* is *back in stock* at {SHOP_NAME}!{price_text}

🏃 _Hurry! Limited quantity available!_

Visit us or reply to reserve yours!

~ Team {SHOP_NAME}"""


# =============================================
# 6. WARRANTY REMINDER
# =============================================
def warranty_reminder(customer_name, product_name, warranty_end_date):
    return f"""⚠️ *Warranty Reminder* ⚠️

Dear {customer_name} ji,

Your warranty for *{product_name}* purchased from {SHOP_NAME} is expiring on *{warranty_end_date}*.

💡 If you have any issues with the product, please visit us before the warranty expires!

We can also help with *extended warranty* options.

~ Team {SHOP_NAME}"""


# =============================================
# 7. PRICE DROP ALERT
# =============================================
def price_drop_alert(customer_name, product_name, old_price, new_price):
    discount = round((1 - new_price/old_price) * 100)
    savings = old_price - new_price
    return f"""📉 *PRICE DROP ALERT!* 📉

Dear {customer_name} ji,

*{product_name}*
~~₹{old_price:,}~~ → *₹{new_price:,}*

💰 Save ₹{savings:,} ({discount}% OFF!)

📍 Available at *{SHOP_NAME}*
⏰ _While stocks last!_

~ Team {SHOP_NAME}"""


# =============================================
# 8. REORDER REMINDER (for consumables)
# =============================================
def reorder_reminder(customer_name, product_name, last_purchase_date):
    return f"""🔄 *Time to Reorder?* 🔄

Dear {customer_name} ji,

You purchased *{product_name}* from us on {last_purchase_date}.

It might be time for a replacement/refill! 

📍 Visit *{SHOP_NAME}* or reply here to place an order.
🚗 Home delivery available!

~ Team {SHOP_NAME}"""


# =============================================
# 9. MONSOON SAFETY TIPS (Engagement content)
# =============================================
def safety_tips_monsoon():
    return f"""⚡ *Monsoon Electrical Safety Tips* ⚡
by *{SHOP_NAME}*

Stay safe this rainy season! 🌧️

1️⃣ Check all electrical connections for water leakage
2️⃣ Use MCB/ELCB for safety against short circuits
3️⃣ Avoid using damaged switches or wires
4️⃣ Keep electrical appliances away from water
5️⃣ Use waterproof fittings in outdoor areas
6️⃣ Get your wiring checked before monsoon

🔌 *Need electrical safety products?*
Visit *{SHOP_NAME}* for:
✔️ MCBs & ELCBs
✔️ Waterproof fittings
✔️ Surge protectors
✔️ Quality wires & cables

Stay safe! ⚡🙏
~ Team {SHOP_NAME}"""


# =============================================
# 10. ENERGY SAVING TIPS (Engagement content)
# =============================================
def energy_saving_tips():
    return f"""💡 *Energy Saving Tips* 💡
by *{SHOP_NAME}*

Save electricity, save money! 💰

1️⃣ Switch to *LED lights* - save up to 80% power
2️⃣ Use *5-star rated* fans & appliances
3️⃣ Turn off appliances when not in use
4️⃣ Use *timer switches* for outdoor lights
5️⃣ Set AC temperature to 24°C
6️⃣ Use *solar-powered* outdoor lighting

🏪 *{SHOP_NAME}* has all energy-efficient products!
Visit us to upgrade and save on your electricity bill!

💡 Go green, save money! 🌱
~ Team {SHOP_NAME}"""


# =============================================
# 11. GOOGLE REVIEW REQUEST
# =============================================
def review_request(customer_name):
    return f"""⭐ *Rate Us on Google!* ⭐

Dear {customer_name} ji,

Thank you for choosing *{SHOP_NAME}!* 🙏

If you're happy with our products & service, please take a moment to leave us a *Google Review*:

🔗 [Your Google Maps Link Here]

Your review helps us grow and serve you better! 🌟

Thank you! 🙏
~ Team {SHOP_NAME}"""


# =============================================
# 12. EMI / FINANCE AVAILABLE
# =============================================
def emi_available(customer_name):
    return f"""💳 *EMI Now Available at {SHOP_NAME}!* 💳

Dear {customer_name} ji,

Great news! Now buy your favourite electrical products on *Easy EMI!* 🎉

✅ 0% interest on select items
✅ 3/6/9/12 month EMI options
✅ All major credit cards accepted
✅ Bajaj Finserv EMI card accepted

Products available on EMI:
⚡ Inverters & UPS
🌀 Premium Fans
💡 Chandeliers & Decorative Lights
🔧 Motors & Pumps

Visit *{SHOP_NAME}* today!

~ Team {SHOP_NAME}"""


# =============================================
# TEMPLATE INDEX (for quick access)
# =============================================
ALL_TEMPLATES = {
    "welcome": {"name": "Welcome Message", "func": "welcome_message", "args": ["customer_name"]},
    "shop_info": {"name": "Shop Information", "func": "shop_info_message", "args": []},
    "offer": {"name": "Special Offer", "func": "offer_message", "args": ["customer_name", "offer_text"]},
    "enquiry": {"name": "Enquiry Follow-up", "func": "enquiry_followup", "args": ["customer_name", "product_name"]},
    "back_in_stock": {"name": "Back in Stock Alert", "func": "back_in_stock", "args": ["customer_name", "product_name"]},
    "warranty": {"name": "Warranty Reminder", "func": "warranty_reminder", "args": ["customer_name", "product_name", "warranty_end_date"]},
    "price_drop": {"name": "Price Drop Alert", "func": "price_drop_alert", "args": ["customer_name", "product_name", "old_price", "new_price"]},
    "reorder": {"name": "Reorder Reminder", "func": "reorder_reminder", "args": ["customer_name", "product_name", "last_purchase_date"]},
    "safety_monsoon": {"name": "Monsoon Safety Tips", "func": "safety_tips_monsoon", "args": []},
    "energy_tips": {"name": "Energy Saving Tips", "func": "energy_saving_tips", "args": []},
    "review": {"name": "Google Review Request", "func": "review_request", "args": ["customer_name"]},
    "emi": {"name": "EMI Available", "func": "emi_available", "args": ["customer_name"]},
}
