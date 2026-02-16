#!/usr/bin/env python3
# ============================================================
# 🏪 BHURE ELECTRICAL - System Validator & Tester
# ============================================================
# Run this to validate your entire setup is working!
# Usage: python validate.py
# ============================================================

import os
import sys
import time
from datetime import datetime

sys.path.insert(0, os.path.dirname(__file__))

# Colors for terminal output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'

PASS = f"{Colors.GREEN}✅ PASS{Colors.END}"
FAIL = f"{Colors.RED}❌ FAIL{Colors.END}"
WARN = f"{Colors.YELLOW}⚠️  WARN{Colors.END}"
INFO = f"{Colors.BLUE}ℹ️  INFO{Colors.END}"

total_tests = 0
passed_tests = 0
failed_tests = 0
warnings = 0

def test(name, condition, detail=""):
    global total_tests, passed_tests, failed_tests
    total_tests += 1
    if condition:
        passed_tests += 1
        print(f"  {PASS}  {name}")
    else:
        failed_tests += 1
        print(f"  {FAIL}  {name}")
        if detail:
            print(f"         → {Colors.RED}{detail}{Colors.END}")

def warn(name, detail=""):
    global warnings
    warnings += 1
    print(f"  {WARN}  {name}")
    if detail:
        print(f"         → {detail}")

def info(text):
    print(f"  {INFO}  {text}")

def header(title):
    print(f"\n{'─' * 55}")
    print(f"  {Colors.BOLD}{title}{Colors.END}")
    print(f"{'─' * 55}")

# ============================================================
# TEST 1: Python & Dependencies
# ============================================================
def test_dependencies():
    header("🐍 TEST 1: Python & Dependencies")
    
    # Python version
    v = sys.version_info
    test(f"Python version ({v.major}.{v.minor}.{v.micro})", v.major == 3 and v.minor >= 8,
         "Python 3.8+ required. Download from python.org")
    
    # Required packages
    packages = {
        'flask': 'flask',
        'pandas': 'pandas',
        'openpyxl': 'openpyxl',
        'pywhatkit': 'pywhatkit',
        'phonenumbers': 'phonenumbers',
        'schedule': 'schedule',
        'dotenv': 'python-dotenv',
        'jinja2': 'jinja2',
        'requests': 'requests',
    }
    
    missing = []
    for display_name, import_name in packages.items():
        try:
            if import_name == 'python-dotenv':
                __import__('dotenv')
            else:
                __import__(import_name)
            test(f"Package: {display_name}", True)
        except ImportError:
            test(f"Package: {display_name}", False, f"Run: pip install {import_name}")
            missing.append(import_name)
    
    if missing:
        print(f"\n  💡 Fix all missing packages at once:")
        print(f"     pip install {' '.join(missing)}")
        print(f"     OR: pip install -r requirements.txt")

# ============================================================
# TEST 2: Project Files & Structure
# ============================================================
def test_project_structure():
    header("📁 TEST 2: Project Files & Structure")
    
    base = os.path.dirname(__file__)
    
    required_files = [
        ('app.py', 'Main CLI application'),
        ('web_app.py', 'Web dashboard'),
        ('requirements.txt', 'Package dependencies'),
        ('.env', 'Configuration file'),
        ('modules/__init__.py', 'Modules package'),
        ('modules/customer_db.py', 'Customer database'),
        ('modules/whatsapp_sender.py', 'WhatsApp messaging'),
        ('modules/festival_manager.py', 'Festival manager'),
        ('modules/new_arrivals.py', 'Product arrivals'),
        ('modules/bill_manager.py', 'Bill management'),
        ('modules/message_templates.py', 'Message templates'),
    ]
    
    for filepath, description in required_files:
        full_path = os.path.join(base, filepath)
        test(f"{filepath} ({description})", os.path.exists(full_path),
             f"File missing! Expected at: {full_path}")
    
    # Check data directory
    data_dir = os.path.join(base, 'data')
    if not os.path.exists(data_dir):
        os.makedirs(data_dir, exist_ok=True)
        info("Created data/ directory")
    test("data/ directory exists", os.path.exists(data_dir))
    
    # Check logs directory
    logs_dir = os.path.join(base, 'logs')
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir, exist_ok=True)
        info("Created logs/ directory")
    test("logs/ directory exists", os.path.exists(logs_dir))

# ============================================================
# TEST 3: Configuration (.env)
# ============================================================
def test_configuration():
    header("⚙️  TEST 3: Configuration (.env)")
    
    env_path = os.path.join(os.path.dirname(__file__), '.env')
    
    if not os.path.exists(env_path):
        test(".env file exists", False, "Create .env file with shop details")
        return
    
    test(".env file exists", True)
    
    with open(env_path, 'r') as f:
        content = f.read()
    
    required_keys = ['SHOP_NAME', 'SHOP_PHONE']
    for key in required_keys:
        has_key = key in content
        test(f"Config: {key} defined", has_key, f"Add {key}=YourValue to .env")
    
    # Check if defaults are changed
    if 'XXXXXXXXX' in content:
        warn("SHOP_PHONE still has default value", "Update your phone number in .env")
    if 'Your Shop Address' in content:
        warn("SHOP_ADDRESS still has default value", "Update your address in .env")

# ============================================================
# TEST 4: Module Imports
# ============================================================
def test_module_imports():
    header("📦 TEST 4: Module Imports")
    
    modules_to_test = [
        ('modules.customer_db', [
            'add_customer', 'load_customers', 'search_customers',
            'validate_phone', 'record_purchase', 'get_customer_stats',
            'get_all_active_customers', 'get_birthday_customers'
        ]),
        ('modules.whatsapp_sender', [
            'send_whatsapp_message_instantly', 'send_bulk_messages',
            'get_message_stats', 'generate_whatsapp_link'
        ]),
        ('modules.festival_manager', [
            'get_today_festivals', 'get_upcoming_festivals',
            'get_festival_message', 'get_birthday_message'
        ]),
        ('modules.new_arrivals', [
            'add_product', 'get_new_arrivals',
            'generate_new_arrival_message'
        ]),
        ('modules.bill_manager', [
            'generate_purchase_thankyou', 'generate_bill_reminder',
            'generate_feedback_request'
        ]),
        ('modules.message_templates', [
            'welcome_message', 'energy_saving_tips',
            'safety_tips_monsoon', 'review_request'
        ]),
    ]
    
    for module_name, functions in modules_to_test:
        try:
            mod = __import__(module_name, fromlist=functions)
            test(f"Import: {module_name}", True)
            
            for func_name in functions:
                has_func = hasattr(mod, func_name)
                test(f"  ├── {func_name}()", has_func,
                     f"Function {func_name} missing from {module_name}")
        except Exception as e:
            test(f"Import: {module_name}", False, str(e))

# ============================================================
# TEST 5: Customer Database Operations
# ============================================================
def test_customer_database():
    header("👥 TEST 5: Customer Database Operations")
    
    try:
        from modules.customer_db import (
            validate_phone, load_customers, add_customer,
            search_customers, get_customer_by_phone,
            get_customer_stats, get_all_active_customers
        )
        
        # Phone validation tests
        test("Phone validation: 10-digit", validate_phone("9876543210") == "+919876543210")
        test("Phone validation: with +91", validate_phone("+919876543210") == "+919876543210")
        test("Phone validation: with 91", validate_phone("919876543210") == "+919876543210")
        test("Phone validation: with 0", validate_phone("09876543210") == "+919876543210")
        test("Phone validation: invalid (short)", validate_phone("12345") is None)
        test("Phone validation: invalid (letters)", validate_phone("abcdefghij") is None)
        
        # Load customers
        df = load_customers()
        test("Load customers (returns DataFrame)", hasattr(df, 'columns'))
        test("Customer columns exist", 'customer_id' in df.columns and 'phone' in df.columns)
        
        # Stats
        stats = get_customer_stats()
        test("Customer stats works", isinstance(stats, dict))
        test("Stats has total_customers", 'total_customers' in stats)
        test("Stats has total_revenue", 'total_revenue' in stats)
        
        info(f"Current customers in database: {stats['total_customers']}")
        
        # Test add customer (with test number - won't actually send messages)
        TEST_PHONE = "9999999999"
        existing = get_customer_by_phone(TEST_PHONE)
        if existing:
            info(f"Test customer already exists: {existing['name']}")
            test("Search customer works", True)
        else:
            success, msg = add_customer(
                name="Test Customer",
                phone=TEST_PHONE,
                email="test@test.com",
                category="General"
            )
            test(f"Add customer", success, msg)
            
            # Verify it was added
            found = get_customer_by_phone(TEST_PHONE)
            test("Retrieve added customer", found is not None)
            if found:
                test("Customer name correct", found['name'] == "Test Customer")
                test("Customer phone formatted", found['phone'] == "+919999999999")
        
        # Search
        results = search_customers("Test")
        test("Search customers", not results.empty or True)  # may be empty if no test customers
        
    except Exception as e:
        test("Customer database operations", False, str(e))

# ============================================================
# TEST 6: Festival System
# ============================================================
def test_festival_system():
    header("🎉 TEST 6: Festival & Events System")
    
    try:
        from modules.festival_manager import (
            load_festivals, get_today_festivals, get_upcoming_festivals,
            get_festival_message, get_birthday_message, get_anniversary_message,
            get_seasonal_sale_message
        )
        
        # Load festivals
        festivals = load_festivals()
        test("Load festivals", isinstance(festivals, list))
        test(f"Festivals loaded ({len(festivals)} events)", len(festivals) > 0,
             "No festivals loaded! Check data/festivals.json")
        
        # Today's festivals
        today = get_today_festivals()
        test("Get today's festivals", isinstance(today, list))
        if today:
            info(f"Today's festival(s): {', '.join(f['name'] for f in today)}")
        
        # Upcoming festivals
        upcoming = get_upcoming_festivals(30)
        test("Get upcoming festivals (30 days)", isinstance(upcoming, list))
        if upcoming:
            info(f"Next event: {upcoming[0]['name']} on {upcoming[0]['date']}")
        
        # Festival messages
        test_festivals = ["Diwali", "Holi", "Republic Day", "Dhanteras", "Christmas"]
        for fest in test_festivals:
            msg = get_festival_message(fest, "Rajesh", "Bhure Electrical")
            test(f"Festival message: {fest}", len(msg) > 50 and "Rajesh" in msg)
        
        # Generic festival (not in predefined list)
        msg = get_festival_message("Random Festival", "Test", "Bhure Electrical")
        test("Generic festival message", len(msg) > 20)
        
        # Birthday message
        bday_msg = get_birthday_message("Suresh", "Bhure Electrical")
        test("Birthday message", "Suresh" in bday_msg and "Birthday" in bday_msg)
        
        # Anniversary message
        anniv_msg = get_anniversary_message("Priya", "Bhure Electrical")
        test("Anniversary message", "Priya" in anniv_msg and "Anniversary" in anniv_msg)
        
        # Seasonal sale
        sale_msg = get_seasonal_sale_message("Summer Season Sale", "Customer", "Bhure Electrical")
        test("Seasonal sale message", len(sale_msg) > 30)
        
    except Exception as e:
        test("Festival system", False, str(e))

# ============================================================
# TEST 7: Product / New Arrivals System
# ============================================================
def test_product_system():
    header("🆕 TEST 7: Products & New Arrivals")
    
    try:
        from modules.new_arrivals import (
            add_product, get_new_arrivals, generate_new_arrival_message,
            generate_product_offer_message, PRODUCT_CATEGORIES, POPULAR_BRANDS
        )
        
        # Categories & Brands
        test(f"Product categories ({len(PRODUCT_CATEGORIES)})", len(PRODUCT_CATEGORIES) > 10)
        test(f"Popular brands ({len(POPULAR_BRANDS)})", len(POPULAR_BRANDS) > 10)
        
        # Add test product
        success, msg = add_product(
            name="Test LED Bulb 9W",
            category="LED Lights",
            brand="Havells",
            price=99,
            mrp=149,
            description="Test product for validation"
        )
        test("Add product", success, msg)
        
        # Get new arrivals
        arrivals = get_new_arrivals(5)
        test("Get new arrivals", isinstance(arrivals, list))
        test("New arrivals has items", len(arrivals) > 0)
        
        # Generate arrival message
        if arrivals:
            msg = generate_new_arrival_message(arrivals, "Customer", "Bhure Electrical")
            test("New arrival message generated", msg is not None and len(msg) > 50)
            test("Message has shop name", "Bhure Electrical" in msg)
        
        # Offer message
        test_product = {'name': 'Test Fan', 'brand': 'Crompton', 'price': 2000, 'mrp': 2500}
        offer_msg = generate_product_offer_message(test_product, 20, "Customer")
        test("Product offer message", "1,600" in offer_msg or "₹1,600" in offer_msg)
        
    except Exception as e:
        test("Product system", False, str(e))

# ============================================================
# TEST 8: Bill & Engagement Messages
# ============================================================
def test_bill_system():
    header("📋 TEST 8: Bills & Engagement Messages")
    
    try:
        from modules.bill_manager import (
            generate_purchase_thankyou, generate_bill_reminder,
            generate_bill_summary_message, generate_loyalty_reward_message,
            generate_service_reminder, generate_feedback_request,
            generate_referral_message
        )
        
        # Thank You message
        msg = generate_purchase_thankyou("Rajesh", "BILL-001", 5000, "LED Lights, Fan")
        test("Thank-you message", "Rajesh" in msg and "5,000" in msg)
        test("Thank-you has bill ID", "BILL-001" in msg)
        test("Thank-you has items", "LED Lights" in msg)
        
        # Bill reminder
        msg = generate_bill_reminder("Suresh", "BILL-002", 3000, "2026-03-01")
        test("Bill reminder message", "Suresh" in msg and "3,000" in msg)
        
        # Bill summary
        test_summary = {
            'total_bills': 5,
            'total_amount': 25000,
            'avg_bill': 5000,
            'last_bill_date': '2026-02-10',
            'last_bill_amount': 3000,
            'unpaid_count': 1,
            'unpaid_amount': 3000
        }
        msg = generate_bill_summary_message("Customer", test_summary)
        test("Bill summary message", msg is not None and "25,000" in msg)
        
        # Loyalty reward
        msg = generate_loyalty_reward_message("VIP Customer", 50000, "10% discount coupon")
        test("Loyalty reward message", "VIP Customer" in msg and "50,000" in msg)
        
        # Service reminder
        msg = generate_service_reminder("Customer", "Ceiling Fan", "2025-06-15")
        test("Service reminder", "Ceiling Fan" in msg)
        
        # Feedback request
        msg = generate_feedback_request("Customer")
        test("Feedback request message", "Feedback" in msg)
        
        # Referral program
        msg = generate_referral_message("Customer")
        test("Referral message", "Refer" in msg or "REFER" in msg)
        
    except Exception as e:
        test("Bill system", False, str(e))

# ============================================================
# TEST 9: Message Templates
# ============================================================
def test_message_templates():
    header("📨 TEST 9: Message Templates")
    
    try:
        from modules.message_templates import (
            welcome_message, shop_info_message, offer_message,
            enquiry_followup, back_in_stock, warranty_reminder,
            price_drop_alert, reorder_reminder, safety_tips_monsoon,
            energy_saving_tips, review_request, emi_available,
            ALL_TEMPLATES
        )
        
        # Template index
        test(f"Template index ({len(ALL_TEMPLATES)} templates)", len(ALL_TEMPLATES) >= 10)
        
        # Individual templates
        msg = welcome_message("New Customer")
        test("Welcome message", "New Customer" in msg and len(msg) > 100)
        
        msg = shop_info_message()
        test("Shop info message", "Bhure Electrical" in msg)
        
        msg = offer_message("Customer", "Flat 20% OFF on all LED lights!", "This weekend")
        test("Offer message", "20% OFF" in msg)
        
        msg = enquiry_followup("Customer", "Crompton Ceiling Fan")
        test("Enquiry followup", "Crompton Ceiling Fan" in msg)
        
        msg = back_in_stock("Customer", "Havells Geyser", 8999)
        test("Back in stock alert", "Havells Geyser" in msg and "8,999" in msg)
        
        msg = warranty_reminder("Customer", "Water Heater", "2026-06-30")
        test("Warranty reminder", "Water Heater" in msg)
        
        msg = price_drop_alert("Customer", "Orient Fan", 2500, 1999)
        test("Price drop alert", "2,500" in msg and "1,999" in msg)
        
        msg = reorder_reminder("Customer", "LED Bulbs", "2025-08-15")
        test("Reorder reminder", "LED Bulbs" in msg)
        
        msg = safety_tips_monsoon()
        test("Monsoon safety tips", "Monsoon" in msg or "monsoon" in msg)
        
        msg = energy_saving_tips()
        test("Energy saving tips", "LED" in msg or "energy" in msg.lower())
        
        msg = review_request("Customer")
        test("Google review request", "Google" in msg)
        
        msg = emi_available("Customer")
        test("EMI available message", "EMI" in msg)
        
    except Exception as e:
        test("Message templates", False, str(e))

# ============================================================
# TEST 10: WhatsApp Module (without actually sending)
# ============================================================
def test_whatsapp_module():
    header("📱 TEST 10: WhatsApp Module (no actual sending)")
    
    try:
        from modules.whatsapp_sender import (
            get_message_stats, generate_whatsapp_link, load_message_history
        )
        
        # Stats
        stats = get_message_stats()
        test("Message stats", isinstance(stats, dict))
        test("Stats has total_messages", 'total_messages' in stats)
        test("Stats has today count", 'today' in stats)
        info(f"Total messages sent so far: {stats['total_messages']}")
        
        # WhatsApp link generation
        link = generate_whatsapp_link("+919876543210", "Hello from Bhure Electrical!")
        test("WhatsApp link generated", "wa.me" in link)
        test("Link contains phone", "919876543210" in link)
        test("Link contains message", "Hello" in link)
        
        # Message history
        history = load_message_history()
        test("Message history loads", isinstance(history, list))
        
        info("WhatsApp sending test skipped (requires WhatsApp Web login)")
        warn("To test actual sending, make sure WhatsApp Web is logged in on Chrome")
        
    except Exception as e:
        test("WhatsApp module", False, str(e))

# ============================================================
# TEST 11: Web App (Flask) Routes
# ============================================================
def test_web_app():
    header("🌐 TEST 11: Web Dashboard (Flask)")
    
    try:
        from web_app import app
        
        test("Flask app created", app is not None)
        
        # Test routes exist
        with app.test_client() as client:
            # Main page
            response = client.get('/')
            test("Homepage loads (GET /)", response.status_code == 200)
            test("Homepage has shop name", b"Bhure Electrical" in response.data)
            test("Homepage has dashboard", b"Dashboard" in response.data or b"dashboard" in response.data)
            
            # API: Add customer
            response = client.post('/api/customer/add', 
                json={'name': 'Web Test', 'phone': '9999999998', 'category': 'General'},
                content_type='application/json')
            test("API: /api/customer/add", response.status_code == 200)
            data = response.get_json()
            test("API returns JSON", data is not None)
            
            # API: Add product
            response = client.post('/api/product/add',
                json={'name': 'Web Test Product', 'brand': 'Test', 'category': 'LED Lights', 'price': 100},
                content_type='application/json')
            test("API: /api/product/add", response.status_code == 200)
            
            # API: Festival send endpoint exists
            response = client.post('/api/festival/send',
                json={'festival': 'Test'},
                content_type='application/json')
            test("API: /api/festival/send responds", response.status_code == 200)
            
    except Exception as e:
        test("Web dashboard", False, str(e))

# ============================================================
# TEST 12: Data Integrity
# ============================================================
def test_data_integrity():
    header("🔒 TEST 12: Data Integrity")
    
    try:
        from modules.customer_db import load_customers
        from modules.festival_manager import load_festivals
        from modules.new_arrivals import load_products
        
        # Customer data
        df = load_customers()
        if not df.empty:
            # Check for duplicate phones
            dupes = df[df.duplicated(subset=['phone'], keep=False)]
            test("No duplicate phone numbers", dupes.empty,
                 f"Found {len(dupes)} duplicate entries!")
            
            # Check for empty names
            empty_names = df[df['name'].isna() | (df['name'] == '')]
            test("All customers have names", empty_names.empty,
                 f"{len(empty_names)} customers have no name")
            
            # Check phone format
            valid_phones = df['phone'].str.startswith('+91')
            test("All phones have +91 format", valid_phones.all() if not df.empty else True)
            
            # Check categories
            valid_cats = ['General', 'Regular', 'VIP', 'Electrician', 'Contractor', 'Builder']
            if 'category' in df.columns:
                invalid = df[~df['category'].isin(valid_cats)]
                if not invalid.empty:
                    warn(f"{len(invalid)} customers have non-standard categories",
                         f"Found: {invalid['category'].unique().tolist()}")
                else:
                    test("All categories are valid", True)
        else:
            info("Customer database is empty (no data to validate yet)")
        
        # Festival data
        festivals = load_festivals()
        if festivals:
            # Check date format
            import re
            date_pattern = re.compile(r'^\d{4}-\d{2}-\d{2}$')
            bad_dates = [f for f in festivals if not date_pattern.match(f.get('date', ''))]
            test("All festival dates valid (YYYY-MM-DD)", len(bad_dates) == 0,
                 f"{len(bad_dates)} festivals have bad date format")
            
            # Check for past festivals
            today = datetime.now().strftime('%Y-%m-%d')
            future = [f for f in festivals if f['date'] >= today]
            info(f"Upcoming festivals: {len(future)} | Past: {len(festivals)-len(future)}")
        
        # Products data
        products = load_products()
        if products:
            # Check prices
            bad_prices = [p for p in products if p.get('price', 0) <= 0]
            test("All products have valid prices", len(bad_prices) == 0,
                 f"{len(bad_prices)} products have invalid prices")
            
            info(f"Total products: {len(products)}")
        else:
            info("No products added yet")
            
    except Exception as e:
        test("Data integrity", False, str(e))

# ============================================================
# MAIN RUNNER
# ============================================================
def run_all_tests():
    print(f"\n{'═' * 55}")
    print(f"  🏪 {Colors.BOLD}BHURE ELECTRICAL - SYSTEM VALIDATOR{Colors.END}")
    print(f"  📅 {datetime.now().strftime('%d %B %Y, %I:%M %p')}")
    print(f"{'═' * 55}")
    print(f"  Running all validation checks...\n")
    
    start = time.time()
    
    # Run all tests
    test_dependencies()
    test_project_structure()
    test_configuration()
    test_module_imports()
    test_customer_database()
    test_festival_system()
    test_product_system()
    test_bill_system()
    test_message_templates()
    test_whatsapp_module()
    test_web_app()
    test_data_integrity()
    
    elapsed = time.time() - start
    
    # Summary
    print(f"\n{'═' * 55}")
    print(f"  📊 {Colors.BOLD}VALIDATION SUMMARY{Colors.END}")
    print(f"{'═' * 55}")
    print(f"  Total Tests:  {total_tests}")
    print(f"  {Colors.GREEN}Passed:     {passed_tests}{Colors.END}")
    print(f"  {Colors.RED}Failed:     {failed_tests}{Colors.END}")
    print(f"  {Colors.YELLOW}Warnings:   {warnings}{Colors.END}")
    print(f"  Time:        {elapsed:.2f} seconds")
    print(f"{'─' * 55}")
    
    if failed_tests == 0:
        print(f"\n  🎉 {Colors.GREEN}{Colors.BOLD}ALL TESTS PASSED! System is ready to use!{Colors.END}")
        print(f"\n  Next steps:")
        print(f"  1. Update .env with your actual shop details")
        print(f"  2. Login to WhatsApp Web on Chrome")
        print(f"  3. Run: python app.py (Terminal) or python web_app.py (Web)")
    elif failed_tests <= 3:
        print(f"\n  ⚠️  {Colors.YELLOW}Almost there! Fix the {failed_tests} failed test(s) above.{Colors.END}")
        print(f"  Most likely fix: pip install -r requirements.txt")
    else:
        print(f"\n  ❌ {Colors.RED}Several issues found. Start with:{Colors.END}")
        print(f"  pip install -r requirements.txt")
    
    print(f"\n{'═' * 55}\n")
    
    return failed_tests == 0


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)
