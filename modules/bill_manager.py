# ============================================
# Bhure Electrical - Bill & Payment Reminders
# ============================================
# Send bill summaries, payment reminders, and purchase thank you messages

import os
import pandas as pd
from datetime import datetime, timedelta

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
BILLS_FILE = os.path.join(DATA_DIR, 'bills.xlsx')

def load_bills():
    """Load bills database"""
    os.makedirs(DATA_DIR, exist_ok=True)
    if os.path.exists(BILLS_FILE):
        return pd.read_excel(BILLS_FILE)
    return pd.DataFrame(columns=[
        'bill_id', 'customer_phone', 'customer_name', 'amount',
        'items', 'date', 'is_paid', 'payment_mode', 'due_date'
    ])

def get_recent_bills(phone=None, days=30):
    """Get recent bills, optionally filtered by customer phone"""
    df = load_bills()
    if df.empty:
        return df
    
    cutoff = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
    
    if phone:
        return df[(df['customer_phone'] == phone) & (df['date'] >= cutoff)]
    return df[df['date'] >= cutoff]

def get_unpaid_bills():
    """Get all unpaid/pending bills"""
    df = load_bills()
    if df.empty:
        return df
    return df[df['is_paid'] == False]

def get_customer_bill_summary(phone):
    """Get bill summary for a customer"""
    df = load_bills()
    if df.empty:
        return None
    
    customer_bills = df[df['customer_phone'] == phone]
    if customer_bills.empty:
        return None
    
    return {
        'total_bills': len(customer_bills),
        'total_amount': customer_bills['amount'].sum(),
        'avg_bill': customer_bills['amount'].mean(),
        'last_bill_date': customer_bills['date'].max(),
        'last_bill_amount': customer_bills.iloc[-1]['amount'],
        'unpaid_count': len(customer_bills[customer_bills['is_paid'] == False]),
        'unpaid_amount': customer_bills[customer_bills['is_paid'] == False]['amount'].sum()
    }

# =============================================
# MESSAGE GENERATORS
# =============================================

def generate_purchase_thankyou(customer_name, bill_id, amount, items='', shop_name="Bhure Electrical"):
    """Generate thank you message after purchase"""
    items_text = f"\n📦 Items: {items}" if items else ""
    
    return f"""🙏 *Thank You for Your Purchase!* 🙏

Dear {customer_name} ji,

Thank you for shopping at *{shop_name}!* 🏪

📋 *Bill Details:*
🆔 Bill No: {bill_id}
💰 Amount: ₹{amount:,.0f}{items_text}
📅 Date: {datetime.now().strftime('%d %B %Y')}

We value your trust in us! 

💡 _For any product support or queries, feel free to message us on WhatsApp!_

⭐ If you liked our service, please recommend *{shop_name}* to your friends & family!

Thank you! 🙏
~ Team {shop_name}"""

def generate_bill_reminder(customer_name, bill_id, amount, due_date, shop_name="Bhure Electrical"):
    """Generate payment reminder for unpaid bills"""
    return f"""📋 *Payment Reminder* 📋

Dear {customer_name} ji,

This is a gentle reminder about your pending payment:

🆔 Bill No: {bill_id}
💰 Amount Due: ₹{amount:,.0f}
📅 Due Date: {due_date}

Please visit *{shop_name}* to clear the payment at your convenience.

💳 Payment modes: Cash / UPI / Card

Thank you! 🙏
~ Team {shop_name}"""

def generate_bill_summary_message(customer_name, summary, shop_name="Bhure Electrical"):
    """Generate monthly/quarterly bill summary"""
    if not summary:
        return None
    
    unpaid_text = ""
    if summary['unpaid_count'] > 0:
        unpaid_text = f"\n\n⚠️ *Pending Amount: ₹{summary['unpaid_amount']:,.0f}* ({summary['unpaid_count']} bills)"
    
    return f"""📊 *Your Purchase Summary at {shop_name}* 📊

Dear {customer_name} ji,

Here's your shopping summary with us:

📋 Total Bills: {summary['total_bills']}
💰 Total Spent: ₹{summary['total_amount']:,.0f}
📅 Last Visit: {summary['last_bill_date']}{unpaid_text}

🌟 *You are a valued customer!*

Thank you for choosing {shop_name}! 🙏
~ Team {shop_name}"""

def generate_loyalty_reward_message(customer_name, total_spent, reward, shop_name="Bhure Electrical"):
    """Generate loyalty/reward message for high-value customers"""
    return f"""🌟 *LOYALTY REWARD for You!* 🌟

Dear {customer_name} ji,

*Congratulations!* 🎉

Your total purchases at *{shop_name}* have crossed *₹{total_spent:,.0f}!*

As a token of appreciation, you've earned:
🎁 *{reward}*

Visit *{shop_name}* to claim your reward!

Thank you for your loyalty! 🙏
~ Team {shop_name}"""

def generate_service_reminder(customer_name, product_name, purchase_date, shop_name="Bhure Electrical"):
    """Generate service/maintenance reminder"""
    return f"""🔧 *Service Reminder* 🔧

Dear {customer_name} ji,

It's been a while since you purchased *{product_name}* from us on {purchase_date}.

Time for a *routine service/check-up*! ✅

Regular maintenance keeps your products running efficiently and increases their lifespan!

📞 Contact *{shop_name}* to schedule a service visit.

~ Team {shop_name}"""

def generate_feedback_request(customer_name, shop_name="Bhure Electrical"):
    """Generate feedback request message"""
    return f"""⭐ *We Value Your Feedback!* ⭐

Dear {customer_name} ji,

Thank you for shopping at *{shop_name}!*

We'd love to hear about your experience:

1️⃣ How was our service? (Excellent / Good / Average)
2️⃣ Did you find what you needed?
3️⃣ Any suggestions for us?

Your feedback helps us serve you better! 🙏

_Simply reply to this message with your feedback!_

~ Team {shop_name}"""

def generate_referral_message(customer_name, shop_name="Bhure Electrical"):
    """Generate referral program message"""
    return f"""🎁 *REFER & EARN at {shop_name}!* 🎁

Dear {customer_name} ji,

*Good news!* We've started a referral program! 🎉

📣 *How it works:*
1️⃣ Refer a friend/family to *{shop_name}*
2️⃣ They make a purchase & mention your name
3️⃣ *You BOTH get 5% OFF* on your next purchase!

It's that simple! 💪

Share *{shop_name}* with your loved ones and save together!

~ Team {shop_name}"""
