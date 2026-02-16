# ============================================
# Bhure Electrical - Customer Database Manager
# ============================================
# Manages customer data: add, update, search, import/export

import os
import json
import pandas as pd
from datetime import datetime, timedelta
import phonenumbers

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
CUSTOMERS_FILE = os.path.join(DATA_DIR, 'customers.xlsx')
BILLS_FILE = os.path.join(DATA_DIR, 'bills.xlsx')

def ensure_data_dir():
    """Create data directory if it doesn't exist"""
    os.makedirs(DATA_DIR, exist_ok=True)

def validate_phone(phone):
    """Validate and format Indian phone number"""
    try:
        phone = str(phone).strip()
        if not phone.startswith('+'):
            if phone.startswith('91'):
                phone = '+' + phone
            elif phone.startswith('0'):
                phone = '+91' + phone[1:]
            else:
                phone = '+91' + phone
        parsed = phonenumbers.parse(phone)
        if phonenumbers.is_valid_number(parsed):
            return phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164)
    except:
        pass
    return None

def load_customers():
    """Load customer database from Excel"""
    ensure_data_dir()
    if os.path.exists(CUSTOMERS_FILE):
        df = pd.read_excel(CUSTOMERS_FILE)
        # Ensure phone column is always string type (Excel may read as numeric)
        # Excel strips the '+' from phones like +919999999999 → 919999999999
        if 'phone' in df.columns:
            df['phone'] = df['phone'].astype(str).apply(
                lambda x: f'+{x}' if x and not x.startswith('+') and x.replace(' ', '').isdigit() else x
            )
        return df
    else:
        df = pd.DataFrame(columns=[
            'customer_id', 'name', 'phone', 'email', 'address',
            'birthday', 'anniversary', 'category', 'tags',
            'total_purchases', 'last_purchase_date', 'last_purchase_amount',
            'total_amount_spent', 'visit_count',
            'added_date', 'notes', 'is_active'
        ])
        df.to_excel(CUSTOMERS_FILE, index=False)
        return df

def save_customers(df):
    """Save customer database to Excel"""
    ensure_data_dir()
    df.to_excel(CUSTOMERS_FILE, index=False)

def add_customer(name, phone, email='', address='', birthday='', 
                 anniversary='', category='General', tags='', notes=''):
    """Add a new customer"""
    df = load_customers()
    
    # Validate phone
    formatted_phone = validate_phone(phone)
    if not formatted_phone:
        return False, "Invalid phone number! Please enter a valid Indian mobile number."
    
    # Check duplicate
    if not df.empty and formatted_phone in df['phone'].values:
        return False, f"Customer with phone {formatted_phone} already exists!"
    
    # Generate customer ID
    if df.empty:
        customer_id = 'BE-0001'
    else:
        last_id = df['customer_id'].iloc[-1]
        num = int(last_id.split('-')[1]) + 1
        customer_id = f'BE-{num:04d}'
    
    new_customer = {
        'customer_id': customer_id,
        'name': name.strip().title(),
        'phone': formatted_phone,
        'email': email.strip(),
        'address': address.strip(),
        'birthday': birthday,
        'anniversary': anniversary,
        'category': category,
        'tags': tags,
        'total_purchases': 0,
        'last_purchase_date': '',
        'last_purchase_amount': 0,
        'total_amount_spent': 0,
        'visit_count': 0,
        'added_date': datetime.now().strftime('%Y-%m-%d'),
        'notes': notes,
        'is_active': True
    }
    
    df = pd.concat([df, pd.DataFrame([new_customer])], ignore_index=True)
    save_customers(df)
    return True, f"Customer {name} added successfully! ID: {customer_id}"

def update_customer(phone, **kwargs):
    """Update customer details by phone number"""
    df = load_customers()
    formatted_phone = validate_phone(phone)
    
    if formatted_phone and formatted_phone in df['phone'].values:
        idx = df[df['phone'] == formatted_phone].index[0]
        for key, value in kwargs.items():
            if key in df.columns:
                df.at[idx, key] = value
        save_customers(df)
        return True, "Customer updated successfully!"
    return False, "Customer not found!"

def record_purchase(phone, amount, items=''):
    """Record a purchase for a customer"""
    df = load_customers()
    formatted_phone = validate_phone(phone)
    
    if formatted_phone and formatted_phone in df['phone'].values:
        idx = df[df['phone'] == formatted_phone].index[0]
        df.at[idx, 'total_purchases'] = int(df.at[idx, 'total_purchases'] or 0) + 1
        df.at[idx, 'last_purchase_date'] = datetime.now().strftime('%Y-%m-%d')
        df.at[idx, 'last_purchase_amount'] = amount
        df.at[idx, 'total_amount_spent'] = float(df.at[idx, 'total_amount_spent'] or 0) + amount
        df.at[idx, 'visit_count'] = int(df.at[idx, 'visit_count'] or 0) + 1
        save_customers(df)
        
        # Also record in bills
        record_bill(formatted_phone, df.at[idx, 'name'], amount, items)
        return True, "Purchase recorded!"
    return False, "Customer not found!"

def record_bill(phone, name, amount, items=''):
    """Record a bill"""
    ensure_data_dir()
    if os.path.exists(BILLS_FILE):
        bills_df = pd.read_excel(BILLS_FILE)
    else:
        bills_df = pd.DataFrame(columns=[
            'bill_id', 'customer_phone', 'customer_name', 'amount',
            'items', 'date', 'is_paid', 'payment_mode'
        ])
    
    bill_id = f'BILL-{len(bills_df)+1:05d}'
    new_bill = {
        'bill_id': bill_id,
        'customer_phone': phone,
        'customer_name': name,
        'amount': amount,
        'items': items,
        'date': datetime.now().strftime('%Y-%m-%d %H:%M'),
        'is_paid': True,
        'payment_mode': 'Cash'
    }
    
    bills_df = pd.concat([bills_df, pd.DataFrame([new_bill])], ignore_index=True)
    bills_df.to_excel(BILLS_FILE, index=False)
    return bill_id

def search_customers(query):
    """Search customers by name or phone"""
    df = load_customers()
    if df.empty:
        return df
    
    query = str(query).lower()
    mask = (
        df['name'].astype(str).str.lower().str.contains(query, na=False) |
        df['phone'].astype(str).str.contains(query, na=False)
    )
    return df[mask]

def get_customer_by_phone(phone):
    """Get a single customer by phone"""
    df = load_customers()
    formatted_phone = validate_phone(phone)
    if formatted_phone and not df.empty:
        result = df[df['phone'] == formatted_phone]
        if not result.empty:
            return result.iloc[0].to_dict()
    return None

def get_customers_by_category(category):
    """Get customers filtered by category"""
    df = load_customers()
    if df.empty:
        return df
    return df[df['category'] == category]

def get_recent_customers(days=30):
    """Get customers who purchased in last N days"""
    df = load_customers()
    if df.empty:
        return df
    cutoff = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
    return df[df['last_purchase_date'] >= cutoff]

def get_inactive_customers(days=60):
    """Get customers who haven't purchased in N days"""
    df = load_customers()
    if df.empty:
        return df
    cutoff = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
    return df[(df['last_purchase_date'] < cutoff) | (df['last_purchase_date'] == '')]

def get_birthday_customers(date=None):
    """Get customers with birthday on a given date"""
    df = load_customers()
    if df.empty:
        return df
    if date is None:
        date = datetime.now()
    month_day = date.strftime('%m-%d')
    return df[df['birthday'].astype(str).str.endswith(month_day)]

def get_anniversary_customers(date=None):
    """Get customers with anniversary on a given date"""
    df = load_customers()
    if df.empty:
        return df
    if date is None:
        date = datetime.now()
    month_day = date.strftime('%m-%d')
    return df[df['anniversary'].astype(str).str.endswith(month_day)]

def get_top_customers(n=10):
    """Get top N customers by total spending"""
    df = load_customers()
    if df.empty:
        return df
    return df.nlargest(n, 'total_amount_spent')

def get_all_active_customers():
    """Get all active customers"""
    df = load_customers()
    if df.empty:
        return df
    return df[df['is_active'] == True]

def get_customer_stats():
    """Get overall customer statistics"""
    df = load_customers()
    if df.empty:
        return {
            'total_customers': 0,
            'active_customers': 0,
            'total_revenue': 0,
            'avg_purchase': 0,
            'top_category': 'N/A'
        }
    return {
        'total_customers': len(df),
        'active_customers': len(df[df['is_active'] == True]),
        'total_revenue': df['total_amount_spent'].sum(),
        'avg_purchase': df['total_amount_spent'].mean(),
        'top_category': df['category'].mode()[0] if not df['category'].mode().empty else 'N/A'
    }

def import_customers_from_csv(csv_file):
    """Import customers from a CSV file"""
    try:
        import_df = pd.read_csv(csv_file)
        df = load_customers()
        
        added = 0
        skipped = 0
        for _, row in import_df.iterrows():
            phone = validate_phone(row.get('phone', ''))
            if phone and (df.empty or phone not in df['phone'].values):
                success, _ = add_customer(
                    name=row.get('name', 'Unknown'),
                    phone=row.get('phone', ''),
                    email=row.get('email', ''),
                    address=row.get('address', ''),
                    category=row.get('category', 'General')
                )
                if success:
                    added += 1
                else:
                    skipped += 1
            else:
                skipped += 1
        
        return True, f"Imported {added} customers. Skipped {skipped}."
    except Exception as e:
        return False, f"Import failed: {str(e)}"

def export_customers_to_csv(output_file):
    """Export customers to CSV"""
    df = load_customers()
    df.to_csv(output_file, index=False)
    return True, f"Exported {len(df)} customers to {output_file}"
