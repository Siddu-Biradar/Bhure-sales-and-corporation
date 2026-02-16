#!/usr/bin/env python3
# ============================================================
# 🏪 BHURE ELECTRICAL - Customer Engagement System
# ============================================================
# Main CLI Application - Run this to manage everything!
# 
# Usage: python app.py
# ============================================================

import os
import sys
import time
from datetime import datetime

# Add project root to path
sys.path.insert(0, os.path.dirname(__file__))

from modules.customer_db import (
    add_customer, load_customers, search_customers, update_customer,
    record_purchase, get_recent_customers, get_inactive_customers,
    get_birthday_customers, get_anniversary_customers, get_top_customers,
    get_all_active_customers, get_customer_stats, get_customer_by_phone,
    import_customers_from_csv, export_customers_to_csv
)
from modules.whatsapp_sender import (
    send_whatsapp_message_instantly, send_bulk_messages,
    send_personalized_messages, get_message_stats, generate_whatsapp_link
)
from modules.festival_manager import (
    get_today_festivals, get_upcoming_festivals, get_festival_message,
    get_birthday_message, get_anniversary_message, get_seasonal_sale_message,
    add_festival
)
from modules.new_arrivals import (
    add_product, get_new_arrivals, generate_new_arrival_message,
    PRODUCT_CATEGORIES, POPULAR_BRANDS
)
from modules.bill_manager import (
    generate_purchase_thankyou, generate_bill_reminder,
    generate_feedback_request, generate_referral_message,
    get_customer_bill_summary, generate_bill_summary_message
)
from modules.message_templates import (
    welcome_message, shop_info_message, offer_message,
    safety_tips_monsoon, energy_saving_tips, review_request,
    emi_available, price_drop_alert, back_in_stock,
    enquiry_followup, reorder_reminder, warranty_reminder
)

SHOP_NAME = "Bhure Electrical"

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    print("=" * 60)
    print(f"  🏪 {SHOP_NAME} - Customer Engagement System")
    print(f"  📅 {datetime.now().strftime('%d %B %Y, %A')}")
    print("=" * 60)

def print_menu(title, options):
    print(f"\n{'─' * 50}")
    print(f"  {title}")
    print(f"{'─' * 50}")
    for key, label in options:
        print(f"  [{key}] {label}")
    print(f"{'─' * 50}")

def pause():
    input("\n  Press Enter to continue...")

# =============================================
# MAIN MENU
# =============================================
def main_menu():
    while True:
        clear_screen()
        print_header()
        
        # Show today's alerts
        show_today_alerts()
        
        print_menu("📋 MAIN MENU", [
            ("1", "👥 Customer Management"),
            ("2", "📱 Send WhatsApp Messages"),
            ("3", "🎉 Festival & Event Wishes"),
            ("4", "🆕 New Arrivals & Offers"),
            ("5", "📋 Bills & Reminders"),
            ("6", "📨 Quick Templates"),
            ("7", "📊 Dashboard & Stats"),
            ("8", "⚙️  Settings"),
            ("0", "❌ Exit"),
        ])
        
        choice = input("\n  Enter your choice: ").strip()
        
        if choice == '1':
            customer_menu()
        elif choice == '2':
            whatsapp_menu()
        elif choice == '3':
            festival_menu()
        elif choice == '4':
            product_menu()
        elif choice == '5':
            bill_menu()
        elif choice == '6':
            templates_menu()
        elif choice == '7':
            dashboard()
        elif choice == '8':
            settings_menu()
        elif choice == '0':
            print("\n  👋 Thank you! See you again!")
            print(f"  ~ {SHOP_NAME}")
            sys.exit(0)

def show_today_alerts():
    """Show important alerts for today"""
    alerts = []
    
    # Check today's festivals
    today_festivals = get_today_festivals()
    for f in today_festivals:
        alerts.append(f"  🎉 Today is {f['name']}! {f.get('emoji', '')}")
    
    # Check upcoming festivals
    upcoming = get_upcoming_festivals(3)
    for f in upcoming:
        if f.get('days_until', 0) > 0:
            alerts.append(f"  📅 {f['name']} in {f['days_until']} days {f.get('emoji', '')}")
    
    # Check birthdays
    bday_customers = get_birthday_customers()
    if not bday_customers.empty:
        for _, c in bday_customers.iterrows():
            alerts.append(f"  🎂 Birthday: {c['name']} ({c['phone']})")
    
    # Check anniversaries
    anniv_customers = get_anniversary_customers()
    if not anniv_customers.empty:
        for _, c in anniv_customers.iterrows():
            alerts.append(f"  💍 Anniversary: {c['name']} ({c['phone']})")
    
    if alerts:
        print(f"\n  {'🔔 TODAY\'S ALERTS':}")
        for a in alerts[:5]:
            print(a)

# =============================================
# 1. CUSTOMER MANAGEMENT
# =============================================
def customer_menu():
    while True:
        clear_screen()
        print_header()
        print_menu("👥 CUSTOMER MANAGEMENT", [
            ("1", "➕ Add New Customer"),
            ("2", "🔍 Search Customer"),
            ("3", "📋 View All Customers"),
            ("4", "✏️  Update Customer"),
            ("5", "🛒 Record Purchase"),
            ("6", "📥 Import from CSV"),
            ("7", "📤 Export to CSV"),
            ("8", "🏆 Top Customers"),
            ("0", "⬅️  Back to Main Menu"),
        ])
        
        choice = input("\n  Enter your choice: ").strip()
        
        if choice == '1':
            add_customer_ui()
        elif choice == '2':
            search_customer_ui()
        elif choice == '3':
            view_all_customers()
        elif choice == '4':
            update_customer_ui()
        elif choice == '5':
            record_purchase_ui()
        elif choice == '6':
            import_customers_ui()
        elif choice == '7':
            export_customers_ui()
        elif choice == '8':
            top_customers_ui()
        elif choice == '0':
            break

def add_customer_ui():
    print("\n  ➕ ADD NEW CUSTOMER")
    print("  " + "-" * 40)
    name = input("  Name: ").strip()
    phone = input("  Phone (10 digits): ").strip()
    email = input("  Email (optional): ").strip()
    address = input("  Address (optional): ").strip()
    birthday = input("  Birthday (YYYY-MM-DD, optional): ").strip()
    anniversary = input("  Anniversary (YYYY-MM-DD, optional): ").strip()
    
    print("\n  Categories: General, Electrician, Contractor, Builder, Regular, VIP")
    category = input("  Category [General]: ").strip() or "General"
    
    success, msg = add_customer(name, phone, email, address, birthday, anniversary, category)
    
    if success:
        print(f"\n  ✅ {msg}")
        send_welcome = input("  Send welcome message on WhatsApp? (y/n): ").strip().lower()
        if send_welcome == 'y':
            formatted_phone = get_customer_by_phone(phone)['phone']
            msg = welcome_message(name.title())
            print(f"\n  📱 Sending welcome message to {formatted_phone}...")
            success, result = send_whatsapp_message_instantly(formatted_phone, msg)
            print(f"  {'✅' if success else '❌'} {result}")
    else:
        print(f"\n  ❌ {msg}")
    pause()

def search_customer_ui():
    print("\n  🔍 SEARCH CUSTOMER")
    query = input("  Enter name or phone: ").strip()
    results = search_customers(query)
    
    if results.empty:
        print("  No customers found!")
    else:
        print(f"\n  Found {len(results)} customer(s):")
        print("  " + "-" * 60)
        for _, c in results.iterrows():
            print(f"  {c['customer_id']} | {c['name']:20s} | {c['phone']} | {c.get('category', 'General')}")
    pause()

def view_all_customers():
    df = load_customers()
    if df.empty:
        print("\n  No customers yet! Add your first customer.")
    else:
        print(f"\n  📋 ALL CUSTOMERS ({len(df)} total)")
        print("  " + "-" * 70)
        print(f"  {'ID':10s} {'Name':20s} {'Phone':15s} {'Category':12s} {'Spent':>10s}")
        print("  " + "-" * 70)
        for _, c in df.iterrows():
            spent = f"₹{c.get('total_amount_spent', 0):,.0f}"
            print(f"  {c['customer_id']:10s} {c['name']:20s} {c['phone']:15s} {c.get('category', 'General'):12s} {spent:>10s}")
    pause()

def update_customer_ui():
    phone = input("\n  Enter customer phone to update: ").strip()
    customer = get_customer_by_phone(phone)
    if not customer:
        print("  ❌ Customer not found!")
        pause()
        return
    
    print(f"\n  Updating: {customer['name']} ({customer['phone']})")
    print("  Leave blank to keep current value:")
    
    name = input(f"  Name [{customer['name']}]: ").strip()
    address = input(f"  Address [{customer.get('address', '')}]: ").strip()
    category = input(f"  Category [{customer.get('category', 'General')}]: ").strip()
    
    updates = {}
    if name: updates['name'] = name
    if address: updates['address'] = address
    if category: updates['category'] = category
    
    if updates:
        success, msg = update_customer(phone, **updates)
        print(f"  {'✅' if success else '❌'} {msg}")
    else:
        print("  No changes made.")
    pause()

def record_purchase_ui():
    print("\n  🛒 RECORD PURCHASE")
    phone = input("  Customer phone: ").strip()
    
    customer = get_customer_by_phone(phone)
    if not customer:
        print("  ❌ Customer not found! Add them first.")
        pause()
        return
    
    print(f"  Customer: {customer['name']}")
    amount = float(input("  Bill amount (₹): ").strip())
    items = input("  Items purchased (optional): ").strip()
    
    success, msg = record_purchase(phone, amount, items)
    
    if success:
        print(f"  ✅ {msg}")
        send_thanks = input("  Send thank-you on WhatsApp? (y/n): ").strip().lower()
        if send_thanks == 'y':
            thank_msg = generate_purchase_thankyou(customer['name'], f"BILL-{datetime.now().strftime('%Y%m%d')}", amount, items)
            print(f"  📱 Sending thank-you to {customer['phone']}...")
            s, r = send_whatsapp_message_instantly(customer['phone'], thank_msg)
            print(f"  {'✅' if s else '❌'} {r}")
    else:
        print(f"  ❌ {msg}")
    pause()

def import_customers_ui():
    csv_file = input("\n  Enter CSV file path: ").strip()
    if os.path.exists(csv_file):
        success, msg = import_customers_from_csv(csv_file)
        print(f"  {'✅' if success else '❌'} {msg}")
    else:
        print("  ❌ File not found!")
    pause()

def export_customers_ui():
    output = input("\n  Export filename [customers_export.csv]: ").strip() or "customers_export.csv"
    success, msg = export_customers_to_csv(output)
    print(f"  {'✅' if success else '❌'} {msg}")
    pause()

def top_customers_ui():
    n = int(input("\n  How many top customers? [10]: ").strip() or "10")
    top = get_top_customers(n)
    if top.empty:
        print("  No customers yet!")
    else:
        print(f"\n  🏆 TOP {n} CUSTOMERS BY SPENDING")
        print("  " + "-" * 60)
        for i, (_, c) in enumerate(top.iterrows(), 1):
            medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f" {i}."
            print(f"  {medal} {c['name']:20s} | {c['phone']} | ₹{c['total_amount_spent']:,.0f}")
    pause()

# =============================================
# 2. WHATSAPP MENU
# =============================================
def whatsapp_menu():
    while True:
        clear_screen()
        print_header()
        print_menu("📱 WHATSAPP MESSAGING", [
            ("1", "📤 Send to One Customer"),
            ("2", "📤 Send to All Customers"),
            ("3", "📤 Send to Category (VIP/Regular/etc)"),
            ("4", "📤 Send to Recent Customers"),
            ("5", "📤 Send to Inactive Customers"),
            ("6", "🔗 Generate WhatsApp Link"),
            ("7", "📊 Message Stats"),
            ("0", "⬅️  Back"),
        ])
        
        choice = input("\n  Enter your choice: ").strip()
        
        if choice == '1':
            send_single_ui()
        elif choice == '2':
            send_all_ui()
        elif choice == '3':
            send_category_ui()
        elif choice == '4':
            send_recent_ui()
        elif choice == '5':
            send_inactive_ui()
        elif choice == '6':
            wa_link_ui()
        elif choice == '7':
            show_message_stats()
        elif choice == '0':
            break

def send_single_ui():
    phone = input("\n  Enter phone number: ").strip()
    message = input("  Enter message (or 'template' for templates): ").strip()
    
    if message.lower() == 'template':
        message = choose_template_message()
        if not message:
            return
    
    print(f"\n  📱 Sending to {phone}...")
    success, msg = send_whatsapp_message_instantly(phone, message)
    print(f"  {'✅' if success else '❌'} {msg}")
    pause()

def send_all_ui():
    customers = get_all_active_customers()
    if customers.empty:
        print("\n  No active customers!")
        pause()
        return
    
    print(f"\n  Will send to {len(customers)} customers")
    message = input("  Enter message (or 'template'): ").strip()
    
    if message.lower() == 'template':
        message = choose_template_message()
        if not message:
            return
    
    confirm = input(f"\n  ⚠️ Send to {len(customers)} customers? (yes/no): ").strip().lower()
    if confirm == 'yes':
        phone_list = customers['phone'].tolist()
        results = send_bulk_messages(phone_list, message)
        print(f"\n  ✅ Sent: {results['sent']} | ❌ Failed: {results['failed']}")
    pause()

def send_category_ui():
    category = input("\n  Enter category (General/VIP/Regular/Electrician/Contractor/Builder): ").strip()
    customers = load_customers()
    filtered = customers[customers['category'] == category]
    
    if filtered.empty:
        print(f"  No customers in '{category}' category!")
        pause()
        return
    
    print(f"\n  {len(filtered)} customers in '{category}' category")
    message = input("  Enter message (or 'template'): ").strip()
    
    if message.lower() == 'template':
        message = choose_template_message()
        if not message:
            return
    
    confirm = input(f"\n  Send to {len(filtered)} customers? (yes/no): ").strip().lower()
    if confirm == 'yes':
        phone_list = filtered['phone'].tolist()
        results = send_bulk_messages(phone_list, message)
        print(f"\n  ✅ Sent: {results['sent']} | ❌ Failed: {results['failed']}")
    pause()

def send_recent_ui():
    days = int(input("\n  Customers who purchased in last N days [30]: ").strip() or "30")
    recent = get_recent_customers(days)
    
    if recent.empty:
        print(f"  No customers purchased in last {days} days!")
        pause()
        return
    
    print(f"\n  {len(recent)} recent customers")
    message = input("  Enter message: ").strip()
    
    confirm = input(f"\n  Send to {len(recent)} customers? (yes/no): ").strip().lower()
    if confirm == 'yes':
        phone_list = recent['phone'].tolist()
        results = send_bulk_messages(phone_list, message)
        print(f"\n  ✅ Sent: {results['sent']} | ❌ Failed: {results['failed']}")
    pause()

def send_inactive_ui():
    days = int(input("\n  Inactive for more than N days [60]: ").strip() or "60")
    inactive = get_inactive_customers(days)
    
    if inactive.empty:
        print("  No inactive customers found!")
        pause()
        return
    
    print(f"\n  {len(inactive)} inactive customers")
    
    message = f"""👋 *We Miss You at {SHOP_NAME}!*

Dear Customer,

It's been a while since your last visit! We have lots of new products and exciting offers waiting for you!

🆕 New arrivals every week
🏷️ Special comeback discount - *10% OFF* on your next purchase!

📍 Visit *{SHOP_NAME}* today!
_Show this message to avail the offer_

~ Team {SHOP_NAME}"""
    
    print(f"\n  Default win-back message will be sent.")
    custom = input("  Use custom message instead? (y/n): ").strip().lower()
    if custom == 'y':
        message = input("  Enter your message: ").strip()
    
    confirm = input(f"\n  Send to {len(inactive)} customers? (yes/no): ").strip().lower()
    if confirm == 'yes':
        phone_list = inactive['phone'].tolist()
        results = send_bulk_messages(phone_list, message)
        print(f"\n  ✅ Sent: {results['sent']} | ❌ Failed: {results['failed']}")
    pause()

def wa_link_ui():
    phone = input("\n  Enter phone number: ").strip()
    message = input("  Enter message: ").strip()
    link = generate_whatsapp_link(phone, message)
    print(f"\n  🔗 WhatsApp Link:\n  {link}")
    pause()

def show_message_stats():
    stats = get_message_stats()
    print(f"\n  📊 MESSAGE STATISTICS")
    print(f"  {'─' * 30}")
    print(f"  Total Messages: {stats['total_messages']}")
    print(f"  Sent:           {stats['sent']}")
    print(f"  Failed:         {stats['failed']}")
    print(f"  Today:          {stats['today']}")
    pause()

# =============================================
# 3. FESTIVAL MENU
# =============================================
def festival_menu():
    while True:
        clear_screen()
        print_header()
        print_menu("🎉 FESTIVAL & EVENT WISHES", [
            ("1", "📅 Today's Festivals"),
            ("2", "📅 Upcoming Festivals (7 days)"),
            ("3", "🎉 Send Festival Wishes to All"),
            ("4", "🎂 Send Birthday Wishes"),
            ("5", "💍 Send Anniversary Wishes"),
            ("6", "➕ Add Custom Event"),
            ("0", "⬅️  Back"),
        ])
        
        choice = input("\n  Enter your choice: ").strip()
        
        if choice == '1':
            show_today_festivals()
        elif choice == '2':
            show_upcoming_festivals()
        elif choice == '3':
            send_festival_wishes_ui()
        elif choice == '4':
            send_birthday_wishes_ui()
        elif choice == '5':
            send_anniversary_wishes_ui()
        elif choice == '6':
            add_event_ui()
        elif choice == '0':
            break

def show_today_festivals():
    festivals = get_today_festivals()
    if not festivals:
        print("\n  No festivals today.")
    else:
        print("\n  🎉 TODAY'S FESTIVALS:")
        for f in festivals:
            print(f"  {f.get('emoji', '🎉')} {f['name']} ({f['type']})")
    pause()

def show_upcoming_festivals():
    days = int(input("\n  Show festivals for next N days [7]: ").strip() or "7")
    upcoming = get_upcoming_festivals(days)
    
    if not upcoming:
        print(f"\n  No festivals in next {days} days.")
    else:
        print(f"\n  📅 UPCOMING FESTIVALS ({days} days):")
        for f in upcoming:
            print(f"  {f.get('emoji', '🎉')} {f['date']} - {f['name']} (in {f.get('days_until', '?')} days)")
    pause()

def send_festival_wishes_ui():
    festivals = get_today_festivals()
    
    if not festivals:
        print("\n  No festivals today!")
        manual = input("  Enter festival name manually: ").strip()
        if not manual:
            pause()
            return
        festival_name = manual
    else:
        print("\n  Today's festivals:")
        for i, f in enumerate(festivals, 1):
            print(f"  [{i}] {f['name']}")
        idx = int(input("  Choose festival: ").strip()) - 1
        festival_name = festivals[idx]['name']
    
    customers = get_all_active_customers()
    if customers.empty:
        print("  No customers to send to!")
        pause()
        return
    
    print(f"\n  Will send {festival_name} wishes to {len(customers)} customers")
    confirm = input("  Proceed? (yes/no): ").strip().lower()
    
    if confirm == 'yes':
        messages_to_send = []
        for _, c in customers.iterrows():
            msg = get_festival_message(festival_name, c['name'], SHOP_NAME)
            messages_to_send.append((c['phone'], msg))
        
        results = send_personalized_messages(messages_to_send)
        print(f"\n  ✅ Sent: {results['sent']} | ❌ Failed: {results['failed']}")
    pause()

def send_birthday_wishes_ui():
    bday_customers = get_birthday_customers()
    
    if bday_customers.empty:
        print("\n  No birthdays today!")
        pause()
        return
    
    print(f"\n  🎂 Today's Birthdays:")
    for _, c in bday_customers.iterrows():
        print(f"  🎂 {c['name']} ({c['phone']})")
    
    confirm = input("\n  Send birthday wishes? (yes/no): ").strip().lower()
    if confirm == 'yes':
        for _, c in bday_customers.iterrows():
            msg = get_birthday_message(c['name'], SHOP_NAME)
            print(f"  Sending to {c['name']}...")
            send_whatsapp_message_instantly(c['phone'], msg)
            time.sleep(10)
        print("  ✅ Birthday wishes sent!")
    pause()

def send_anniversary_wishes_ui():
    anniv_customers = get_anniversary_customers()
    
    if anniv_customers.empty:
        print("\n  No anniversaries today!")
        pause()
        return
    
    print(f"\n  💍 Today's Anniversaries:")
    for _, c in anniv_customers.iterrows():
        print(f"  💍 {c['name']} ({c['phone']})")
    
    confirm = input("\n  Send anniversary wishes? (yes/no): ").strip().lower()
    if confirm == 'yes':
        from modules.festival_manager import get_anniversary_message
        for _, c in anniv_customers.iterrows():
            msg = get_anniversary_message(c['name'], SHOP_NAME)
            print(f"  Sending to {c['name']}...")
            send_whatsapp_message_instantly(c['phone'], msg)
            time.sleep(10)
        print("  ✅ Anniversary wishes sent!")
    pause()

def add_event_ui():
    print("\n  ➕ ADD CUSTOM EVENT")
    date = input("  Date (YYYY-MM-DD): ").strip()
    name = input("  Event name: ").strip()
    emoji = input("  Emoji [🎉]: ").strip() or "🎉"
    
    success, msg = add_festival(date, name, emoji=emoji)
    print(f"  {'✅' if success else '❌'} {msg}")
    pause()

# =============================================
# 4. PRODUCT MENU
# =============================================
def product_menu():
    while True:
        clear_screen()
        print_header()
        print_menu("🆕 NEW ARRIVALS & OFFERS", [
            ("1", "➕ Add New Product"),
            ("2", "📋 View New Arrivals"),
            ("3", "📤 Send New Arrivals to All"),
            ("4", "📤 Send Special Offer"),
            ("0", "⬅️  Back"),
        ])
        
        choice = input("\n  Enter your choice: ").strip()
        
        if choice == '1':
            add_product_ui()
        elif choice == '2':
            view_arrivals_ui()
        elif choice == '3':
            send_arrivals_ui()
        elif choice == '4':
            send_offer_ui()
        elif choice == '0':
            break

def add_product_ui():
    print("\n  ➕ ADD NEW PRODUCT")
    name = input("  Product name: ").strip()
    
    print("\n  Categories:", ", ".join(PRODUCT_CATEGORIES[:10]))
    category = input("  Category: ").strip()
    
    print("  Popular brands:", ", ".join(POPULAR_BRANDS[:10]))
    brand = input("  Brand: ").strip()
    
    price = float(input("  Selling price (₹): ").strip())
    mrp = input("  MRP (optional): ").strip()
    mrp = float(mrp) if mrp else price
    description = input("  Description (optional): ").strip()
    
    success, msg = add_product(name, category, brand, price, mrp, description)
    print(f"  {'✅' if success else '❌'} {msg}")
    pause()

def view_arrivals_ui():
    arrivals = get_new_arrivals(10)
    if not arrivals:
        print("\n  No new arrivals yet!")
    else:
        print(f"\n  🆕 NEW ARRIVALS ({len(arrivals)} products):")
        print("  " + "-" * 60)
        for p in arrivals:
            disc = ""
            if p.get('mrp', 0) > p.get('price', 0):
                disc = f" (MRP: ₹{p['mrp']:,})"
            print(f"  {p['id']}. {p['name']} | {p.get('brand', '')} | ₹{p['price']:,}{disc}")
    pause()

def send_arrivals_ui():
    arrivals = get_new_arrivals(5)
    if not arrivals:
        print("\n  No new arrivals to announce!")
        pause()
        return
    
    customers = get_all_active_customers()
    if customers.empty:
        print("  No customers!")
        pause()
        return
    
    print(f"\n  Will announce {len(arrivals)} new products to {len(customers)} customers")
    confirm = input("  Proceed? (yes/no): ").strip().lower()
    
    if confirm == 'yes':
        messages = []
        for _, c in customers.iterrows():
            msg = generate_new_arrival_message(arrivals, c['name'], SHOP_NAME)
            messages.append((c['phone'], msg))
        
        results = send_personalized_messages(messages)
        print(f"\n  ✅ Sent: {results['sent']} | ❌ Failed: {results['failed']}")
    pause()

def send_offer_ui():
    print("\n  📤 SEND SPECIAL OFFER")
    offer_text = input("  Enter offer details: ").strip()
    validity = input("  Offer validity [Limited Period]: ").strip() or "Limited Period"
    
    customers = get_all_active_customers()
    if customers.empty:
        print("  No customers!")
        pause()
        return
    
    print(f"\n  Sending to {len(customers)} customers")
    confirm = input("  Proceed? (yes/no): ").strip().lower()
    
    if confirm == 'yes':
        messages = []
        for _, c in customers.iterrows():
            msg = offer_message(c['name'], offer_text, validity)
            messages.append((c['phone'], msg))
        
        results = send_personalized_messages(messages)
        print(f"\n  ✅ Sent: {results['sent']} | ❌ Failed: {results['failed']}")
    pause()

# =============================================
# 5. BILL MENU
# =============================================
def bill_menu():
    while True:
        clear_screen()
        print_header()
        print_menu("📋 BILLS & REMINDERS", [
            ("1", "📤 Send Bill Thank-You"),
            ("2", "📤 Send Bill Reminder"),
            ("3", "📤 Send Customer Summary"),
            ("4", "📤 Request Feedback"),
            ("5", "📤 Send Referral Program"),
            ("0", "⬅️  Back"),
        ])
        
        choice = input("\n  Enter your choice: ").strip()
        
        if choice == '1':
            bill_thankyou_ui()
        elif choice == '2':
            bill_reminder_ui()
        elif choice == '3':
            bill_summary_ui()
        elif choice == '4':
            feedback_ui()
        elif choice == '5':
            referral_ui()
        elif choice == '0':
            break

def bill_thankyou_ui():
    phone = input("\n  Customer phone: ").strip()
    customer = get_customer_by_phone(phone)
    if not customer:
        print("  ❌ Customer not found!")
        pause()
        return
    
    amount = float(input("  Bill amount (₹): ").strip())
    items = input("  Items (optional): ").strip()
    bill_id = f"BILL-{datetime.now().strftime('%Y%m%d%H%M')}"
    
    msg = generate_purchase_thankyou(customer['name'], bill_id, amount, items)
    print(f"\n  📱 Sending to {customer['phone']}...")
    success, result = send_whatsapp_message_instantly(customer['phone'], msg)
    print(f"  {'✅' if success else '❌'} {result}")
    pause()

def bill_reminder_ui():
    phone = input("\n  Customer phone: ").strip()
    customer = get_customer_by_phone(phone)
    if not customer:
        print("  ❌ Customer not found!")
        pause()
        return
    
    bill_id = input("  Bill ID: ").strip()
    amount = float(input("  Amount due (₹): ").strip())
    due_date = input("  Due date: ").strip()
    
    msg = generate_bill_reminder(customer['name'], bill_id, amount, due_date)
    print(f"\n  📱 Sending to {customer['phone']}...")
    success, result = send_whatsapp_message_instantly(customer['phone'], msg)
    print(f"  {'✅' if success else '❌'} {result}")
    pause()

def bill_summary_ui():
    phone = input("\n  Customer phone: ").strip()
    customer = get_customer_by_phone(phone)
    if not customer:
        print("  ❌ Customer not found!")
        pause()
        return
    
    summary = get_customer_bill_summary(customer['phone'])
    if not summary:
        print("  No billing history for this customer.")
        pause()
        return
    
    msg = generate_bill_summary_message(customer['name'], summary)
    print(f"\n  📱 Sending summary to {customer['phone']}...")
    success, result = send_whatsapp_message_instantly(customer['phone'], msg)
    print(f"  {'✅' if success else '❌'} {result}")
    pause()

def feedback_ui():
    customers = get_recent_customers(7)
    if customers.empty:
        print("\n  No recent customers for feedback!")
        pause()
        return
    
    print(f"\n  Requesting feedback from {len(customers)} recent customers")
    confirm = input("  Proceed? (yes/no): ").strip().lower()
    
    if confirm == 'yes':
        messages = []
        for _, c in customers.iterrows():
            msg = generate_feedback_request(c['name'])
            messages.append((c['phone'], msg))
        
        results = send_personalized_messages(messages)
        print(f"\n  ✅ Sent: {results['sent']} | ❌ Failed: {results['failed']}")
    pause()

def referral_ui():
    customers = get_all_active_customers()
    if customers.empty:
        print("\n  No customers!")
        pause()
        return
    
    print(f"\n  Sending referral program to {len(customers)} customers")
    confirm = input("  Proceed? (yes/no): ").strip().lower()
    
    if confirm == 'yes':
        messages = []
        for _, c in customers.iterrows():
            msg = generate_referral_message(c['name'])
            messages.append((c['phone'], msg))
        
        results = send_personalized_messages(messages)
        print(f"\n  ✅ Sent: {results['sent']} | ❌ Failed: {results['failed']}")
    pause()

# =============================================
# 6. TEMPLATES MENU
# =============================================
def templates_menu():
    while True:
        clear_screen()
        print_header()
        print_menu("📨 QUICK MESSAGE TEMPLATES", [
            ("1", "👋 Welcome Message"),
            ("2", "🏪 Shop Info"),
            ("3", "💡 Energy Saving Tips"),
            ("4", "⚡ Monsoon Safety Tips"),
            ("5", "⭐ Google Review Request"),
            ("6", "💳 EMI Available"),
            ("7", "📉 Price Drop Alert"),
            ("8", "🔔 Back in Stock Alert"),
            ("9", "🔄 Reorder Reminder"),
            ("0", "⬅️  Back"),
        ])
        
        choice = input("\n  Enter your choice: ").strip()
        
        if choice == '0':
            break
        
        template_funcs = {
            '1': ('Welcome', lambda: welcome_message(input("  Customer name: ").strip())),
            '2': ('Shop Info', shop_info_message),
            '3': ('Energy Tips', energy_saving_tips),
            '4': ('Monsoon Safety', safety_tips_monsoon),
            '5': ('Review Request', lambda: review_request(input("  Customer name: ").strip())),
            '6': ('EMI Info', lambda: emi_available(input("  Customer name: ").strip())),
            '7': ('Price Drop', lambda: price_drop_alert(
                input("  Customer name: ").strip(),
                input("  Product name: ").strip(),
                float(input("  Old price: ").strip()),
                float(input("  New price: ").strip())
            )),
            '8': ('Back in Stock', lambda: back_in_stock(
                input("  Customer name: ").strip(),
                input("  Product name: ").strip()
            )),
            '9': ('Reorder', lambda: reorder_reminder(
                input("  Customer name: ").strip(),
                input("  Product name: ").strip(),
                input("  Last purchase date: ").strip()
            )),
        }
        
        if choice in template_funcs:
            name, func = template_funcs[choice]
            msg = func()
            print(f"\n  {'─' * 50}")
            print(f"  📝 {name} Template:")
            print(f"  {'─' * 50}")
            print(msg)
            print(f"  {'─' * 50}")
            
            action = input("\n  [1] Send to one [2] Send to all [3] Copy & go back: ").strip()
            if action == '1':
                phone = input("  Phone number: ").strip()
                send_whatsapp_message_instantly(phone, msg)
                print("  ✅ Sent!")
            elif action == '2':
                customers = get_all_active_customers()
                if not customers.empty:
                    confirm = input(f"  Send to {len(customers)} customers? (yes/no): ").strip().lower()
                    if confirm == 'yes':
                        results = send_bulk_messages(customers['phone'].tolist(), msg)
                        print(f"  ✅ Sent: {results['sent']} | ❌ Failed: {results['failed']}")
        pause()

def choose_template_message():
    """Helper to choose a template message"""
    print("\n  Choose template:")
    print("  [1] Welcome  [2] Shop Info  [3] Energy Tips")
    print("  [4] Safety Tips  [5] EMI Info  [6] Custom")
    
    ch = input("  Choice: ").strip()
    templates = {
        '1': welcome_message("Customer"),
        '2': shop_info_message(),
        '3': energy_saving_tips(),
        '4': safety_tips_monsoon(),
        '5': emi_available("Customer"),
    }
    
    if ch == '6':
        return input("  Enter your message: ").strip()
    return templates.get(ch, None)

# =============================================
# 7. DASHBOARD
# =============================================
def dashboard():
    clear_screen()
    print_header()
    
    c_stats = get_customer_stats()
    m_stats = get_message_stats()
    upcoming = get_upcoming_festivals(7)
    
    print(f"\n  📊 DASHBOARD")
    print(f"  {'═' * 50}")
    
    print(f"\n  👥 CUSTOMERS")
    print(f"  Total: {c_stats['total_customers']} | Active: {c_stats['active_customers']}")
    print(f"  Revenue: ₹{c_stats['total_revenue']:,.0f} | Avg Purchase: ₹{c_stats['avg_purchase']:,.0f}")
    
    print(f"\n  📱 MESSAGES")
    print(f"  Total Sent: {m_stats['total_messages']} | Today: {m_stats['today']}")
    print(f"  Success: {m_stats['sent']} | Failed: {m_stats['failed']}")
    
    if upcoming:
        print(f"\n  📅 UPCOMING EVENTS (7 days)")
        for f in upcoming[:5]:
            print(f"  {f.get('emoji', '🎉')} {f['date']} - {f['name']}")
    
    # Recent customers
    recent = get_recent_customers(7)
    if not recent.empty:
        print(f"\n  🛒 RECENT CUSTOMERS (7 days): {len(recent)}")
    
    # Birthday/Anniversary today
    bdays = get_birthday_customers()
    if not bdays.empty:
        print(f"\n  🎂 BIRTHDAYS TODAY: {len(bdays)}")
    
    pause()

# =============================================
# 8. SETTINGS
# =============================================
def settings_menu():
    clear_screen()
    print_header()
    print(f"""
  ⚙️ SETTINGS
  {'─' * 40}
  
  Current Configuration:
  Shop Name: {SHOP_NAME}
  
  To change settings, edit the .env file
  in the project directory.
  
  📁 Data files are stored in: data/
  📝 Logs are stored in: logs/
  """)
    pause()

# =============================================
# RUN THE APP
# =============================================
if __name__ == '__main__':
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\n\n  👋 Goodbye!")
        sys.exit(0)
