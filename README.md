# 🏪 Bhure Electrical - Customer Engagement System

A complete **WhatsApp-based customer engagement platform** to help Bhure Electrical stay connected with customers through festival wishes, new arrival announcements, bill reminders, offers, and more!

---

## 🌟 Features

### 📱 WhatsApp Messaging
- Send messages to **individual customers** or **bulk send to all**
- Filter by **category** (VIP, Regular, Electrician, Contractor, etc.)
- Target **recent customers** or **re-engage inactive** ones
- **Personalized messages** with customer names
- Generate **WhatsApp links** for easy sharing

### 🎉 Festival & Event Wishes
- **30+ Indian festivals** pre-loaded (Diwali, Holi, Dussehra, etc.)
- **Auto-detect** today's festivals and prompt you to send wishes
- **Birthday & Anniversary** greetings with special discount offers
- **Seasonal sale messages** (Summer, Winter, Monsoon, Diwali)
- Add your own **custom events**

### 🆕 New Product Arrivals
- Add new products with **brand, category, price, MRP**
- Auto-generate **attractive announcement messages**
- Broadcast new arrivals to all customers

### 📋 Bills & Engagement
- **Purchase thank-you** messages
- **Bill reminders** for pending payments
- **Customer bill summaries**
- **Feedback requests** from recent customers
- **Referral program** messages
- **Loyalty rewards** for top customers

### 📨 Ready-to-Use Templates (12+ templates)
- Welcome Message
- Shop Info
- Energy Saving Tips
- Monsoon Safety Tips
- Google Review Request
- EMI/Finance Available
- Price Drop Alert
- Back in Stock Alert
- Reorder Reminder
- Warranty Reminder
- And more!

### 👥 Customer Management
- Add, search, update customers
- Categories: General, VIP, Regular, Electrician, Contractor, Builder
- Track **purchase history** and **total spending**
- Import/Export customers (CSV/Excel)
- Identify **top customers** and **inactive customers**

---

## 🚀 Quick Start

### 1. Install Python (if not installed)
Download from: https://www.python.org/downloads/
Make sure to check "Add Python to PATH" during installation.

### 2. Install Required Packages
Open Terminal/Command Prompt in the project folder and run:
```bash
pip install -r requirements.txt
```

### 3. Setup WhatsApp Web
- Open **Google Chrome**
- Go to **web.whatsapp.com**
- Scan the QR code with your phone
- **Keep it logged in!** (The system uses WhatsApp Web to send messages)

### 4. Configure Your Shop Details
Edit the `.env` file and update:
```
SHOP_NAME=Bhure Electrical
SHOP_PHONE=+91XXXXXXXXXX
SHOP_ADDRESS=Your Shop Address
```

### 5. Run the Application

**Option A: Terminal/CLI App** (recommended for daily use)
```bash
python app.py
```

**Option B: Web Dashboard** (beautiful browser interface)
```bash
python web_app.py
```
Then open http://localhost:5000 in your browser.

---

## 📁 Project Structure

```
Bhure Electrical/
├── app.py                    # Main CLI application
├── web_app.py                # Web dashboard (Flask)
├── requirements.txt          # Python packages
├── .env                      # Shop configuration
├── README.md                 # This file
│
├── modules/
│   ├── __init__.py
│   ├── customer_db.py        # Customer database management
│   ├── whatsapp_sender.py    # WhatsApp message sending
│   ├── festival_manager.py   # Festival wishes & events
│   ├── new_arrivals.py       # Product & arrival management
│   ├── bill_manager.py       # Bills & payment reminders
│   └── message_templates.py  # Ready-to-use message templates
│
├── data/                     # Auto-created data storage
│   ├── customers.xlsx        # Customer database
│   ├── bills.xlsx            # Bill records
│   ├── products.json         # Product catalog
│   └── festivals.json        # Festival calendar
│
└── logs/                     # Message sending logs
    └── message_history.json
```

---

## 📱 How to Use - Daily Workflow

### Morning Routine:
1. **Open the app** (`python app.py`)
2. Check **Today's Alerts** (festivals, birthdays, anniversaries)
3. Send **festival wishes** if it's a special day
4. Send **birthday/anniversary greetings**

### When a Customer Visits:
1. **Add them** to the database (if new)
2. **Record their purchase**
3. Send a **thank-you message** on WhatsApp

### Weekly:
1. Announce **new product arrivals**
2. Send **special offers** to all customers
3. Request **feedback** from recent buyers
4. Check **inactive customers** and send win-back messages

### Monthly:
1. Send **valuable content** (energy tips, safety tips)
2. Promote **referral program**
3. Send **bill summaries** to regular customers
4. Review **dashboard stats**

---

## 💡 Engagement Strategy Tips

| Type | Frequency | Purpose |
|------|-----------|---------|
| Festival Wishes | On festivals | Build personal connection |
| New Arrivals | Weekly/Bi-weekly | Keep customers informed |
| Offers & Deals | 2-3 times/month | Drive sales |
| Tips & Content | Monthly | Build trust & expertise |
| Birthday/Anniversary | On the day | Personal touch |
| Feedback Request | After purchase | Show you care |
| Referral Program | Monthly | Get new customers |
| Bill Reminder | As needed | Professional follow-up |
| Win-back Messages | Monthly | Re-engage lost customers |

---

## ⚠️ Important Notes

1. **WhatsApp Web** must be logged in for messages to send
2. **Don't spam!** Send max 2-3 messages per week to avoid being blocked
3. Messages have a **10-second delay** between sends (to avoid spam detection)
4. **Personalize** messages - use customer names for better engagement
5. **Festival messages** with offers get the best response
6. Always give customers option to **opt-out** if they request

---

## 🆘 Troubleshooting

| Problem | Solution |
|---------|----------|
| Messages not sending | Make sure WhatsApp Web is logged in on Chrome |
| Phone number error | Enter 10-digit number (without +91) or full number with +91 |
| Import not working | Make sure CSV has columns: name, phone, email, address, category |
| Web dashboard not opening | Run `pip install flask` and try again |

---

## 📞 Support

For any issues or customization needs, feel free to ask!

---

*Built with ❤️ for Bhure Electrical*
