# ============================================
# Bhure Electrical - Input Validators
# ============================================
# Reusable validation functions for all user inputs

import re
from datetime import datetime
import phonenumbers


class ValidationError(Exception):
    """Custom validation error with field name and message"""
    def __init__(self, field, message):
        self.field = field
        self.message = message
        super().__init__(f"{field}: {message}")


class Validator:
    """Collection of validation methods. Returns (is_valid, cleaned_value_or_error)"""
    
    # ── Phone Number ──────────────────────────
    @staticmethod
    def phone(value):
        """Validate Indian mobile number. Returns (True, formatted) or (False, error)"""
        if not value:
            return False, "Phone number is required"
        
        value = str(value).strip().replace(' ', '').replace('-', '')
        
        # Remove common prefixes
        if not value.startswith('+'):
            if value.startswith('91') and len(value) == 12:
                value = '+' + value
            elif value.startswith('0'):
                value = '+91' + value[1:]
            elif len(value) == 10:
                value = '+91' + value
            else:
                return False, "Enter a valid 10-digit mobile number"
        
        try:
            parsed = phonenumbers.parse(value)
            if phonenumbers.is_valid_number(parsed):
                formatted = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164)
                return True, formatted
            else:
                return False, "Invalid phone number"
        except Exception:
            return False, "Invalid phone number format"
    
    # ── Name ──────────────────────────────────
    @staticmethod
    def name(value, min_length=2, max_length=100):
        """Validate person/business name"""
        if not value or not str(value).strip():
            return False, "Name is required"
        
        value = str(value).strip()
        
        if len(value) < min_length:
            return False, f"Name must be at least {min_length} characters"
        
        if len(value) > max_length:
            return False, f"Name must be under {max_length} characters"
        
        # Allow letters, spaces, dots, hyphens (Indian names can have these)
        if not re.match(r'^[a-zA-Z\s.\-\']+$', value):
            return False, "Name should contain only letters, spaces, dots, or hyphens"
        
        return True, value.strip().title()
    
    # ── Email ─────────────────────────────────
    @staticmethod
    def email(value, required=False):
        """Validate email address"""
        if not value or not str(value).strip():
            if required:
                return False, "Email is required"
            return True, ""
        
        value = str(value).strip().lower()
        
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if re.match(pattern, value):
            return True, value
        
        return False, "Enter a valid email (e.g., name@example.com)"
    
    # ── Date ──────────────────────────────────
    @staticmethod
    def date(value, required=False, format='%Y-%m-%d'):
        """Validate date string"""
        if not value or not str(value).strip():
            if required:
                return False, "Date is required"
            return True, ""
        
        value = str(value).strip()
        
        # Try multiple common formats
        formats = [
            '%Y-%m-%d',      # 2026-02-16
            '%d-%m-%Y',      # 16-02-2026
            '%d/%m/%Y',      # 16/02/2026
            '%Y/%m/%d',      # 2026/02/16
            '%d %b %Y',      # 16 Feb 2026
            '%d %B %Y',      # 16 February 2026
        ]
        
        for fmt in formats:
            try:
                parsed = datetime.strptime(value, fmt)
                return True, parsed.strftime('%Y-%m-%d')
            except ValueError:
                continue
        
        return False, "Invalid date. Use format: YYYY-MM-DD (e.g., 2026-02-16)"
    
    # ── Amount / Price ────────────────────────
    @staticmethod
    def amount(value, required=True, min_val=0, max_val=10000000):
        """Validate monetary amount"""
        if not value and value != 0:
            if required:
                return False, "Amount is required"
            return True, 0
        
        try:
            # Remove ₹ symbol, commas, spaces
            cleaned = str(value).replace('₹', '').replace(',', '').replace(' ', '').strip()
            amount = float(cleaned)
            
            if amount < min_val:
                return False, f"Amount must be at least ₹{min_val}"
            if amount > max_val:
                return False, f"Amount seems too high (max ₹{max_val:,})"
            
            return True, round(amount, 2)
        except (ValueError, TypeError):
            return False, "Enter a valid amount (e.g., 1500 or 1,500)"
    
    # ── Category ──────────────────────────────
    @staticmethod
    def customer_category(value):
        """Validate customer category"""
        valid = ['General', 'Regular', 'VIP', 'Electrician', 'Contractor', 'Builder']
        
        if not value:
            return True, 'General'
        
        value = str(value).strip().title()
        
        if value in valid:
            return True, value
        
        # Fuzzy match
        for cat in valid:
            if cat.lower().startswith(value.lower()):
                return True, cat
        
        return False, f"Invalid category. Choose from: {', '.join(valid)}"
    
    # ── Product Category ──────────────────────
    @staticmethod
    def product_category(value):
        """Validate product category"""
        valid = [
            "LED Lights", "Ceiling Fans", "Table Fans", "Exhaust Fans",
            "Switches & Sockets", "Wires & Cables", "MCBs & Distribution Boards",
            "Inverters & UPS", "Batteries", "Water Heaters / Geysers",
            "Room Heaters", "Coolers", "Stabilizers", "Decorative Lights",
            "Extension Boards", "Solar Products", "CCTV & Security",
            "Electrical Tools", "Motors & Pumps", "Doorbells"
        ]
        
        if not value:
            return False, "Product category is required"
        
        value = str(value).strip()
        
        # Exact match
        if value in valid:
            return True, value
        
        # Case-insensitive match
        for cat in valid:
            if cat.lower() == value.lower():
                return True, cat
        
        # Partial match
        for cat in valid:
            if value.lower() in cat.lower():
                return True, cat
        
        return True, value  # Allow custom categories
    
    # ── Message Text ──────────────────────────
    @staticmethod
    def message_text(value, max_length=4096):
        """Validate WhatsApp message text"""
        if not value or not str(value).strip():
            return False, "Message cannot be empty"
        
        value = str(value).strip()
        
        if len(value) > max_length:
            return False, f"Message too long ({len(value)} chars). Max: {max_length}"
        
        if len(value) < 2:
            return False, "Message too short"
        
        return True, value
    
    # ── Bill ID ───────────────────────────────
    @staticmethod
    def bill_id(value):
        """Validate bill ID format"""
        if not value:
            return False, "Bill ID is required"
        
        value = str(value).strip().upper()
        
        # Auto-prefix BILL- if not present
        if not value.startswith('BILL-'):
            value = f"BILL-{value}"
        
        return True, value
    
    # ── Address ───────────────────────────────
    @staticmethod
    def address(value, required=False, max_length=500):
        """Validate address"""
        if not value or not str(value).strip():
            if required:
                return False, "Address is required"
            return True, ""
        
        value = str(value).strip()
        
        if len(value) > max_length:
            return False, f"Address too long (max {max_length} chars)"
        
        return True, value
    
    # ── Festival Date ─────────────────────────
    @staticmethod
    def festival_date(value):
        """Validate festival/event date (must be in future)"""
        valid, date_str = Validator.date(value, required=True)
        if not valid:
            return False, date_str
        
        try:
            parsed = datetime.strptime(date_str, '%Y-%m-%d')
            if parsed.date() < datetime.now().date():
                return False, "Date must be in the future"
            return True, date_str
        except:
            return False, "Invalid date"
    
    # ── Discount Percentage ───────────────────
    @staticmethod
    def discount_percent(value):
        """Validate discount percentage"""
        try:
            val = float(str(value).replace('%', '').strip())
            if val < 0 or val > 100:
                return False, "Discount must be between 0% and 100%"
            return True, val
        except (ValueError, TypeError):
            return False, "Enter a valid percentage (e.g., 20)"


# ============================================================
# FORM VALIDATOR (validates multiple fields at once)
# ============================================================
class FormValidator:
    """Validate multiple fields and collect all errors"""
    
    def __init__(self):
        self.errors = {}
        self.cleaned = {}
    
    def validate(self, field_name, validator_func, value, **kwargs):
        """Run a validator and store result"""
        is_valid, result = validator_func(value, **kwargs)
        if is_valid:
            self.cleaned[field_name] = result
        else:
            self.errors[field_name] = result
        return is_valid
    
    @property
    def is_valid(self):
        return len(self.errors) == 0
    
    def get_error_summary(self):
        """Get all errors as a formatted string"""
        if not self.errors:
            return "No errors"
        lines = []
        for field, error in self.errors.items():
            lines.append(f"  ❌ {field}: {error}")
        return "\n".join(lines)
    
    def get_errors_dict(self):
        """Get errors as dictionary (useful for web API)"""
        return self.errors


# ============================================================
# QUICK VALIDATION HELPERS
# ============================================================
def validate_new_customer(name, phone, email='', birthday='', category='General'):
    """Validate all fields for a new customer"""
    form = FormValidator()
    form.validate('name', Validator.name, name)
    form.validate('phone', Validator.phone, phone)
    form.validate('email', Validator.email, email)
    form.validate('birthday', Validator.date, birthday)
    form.validate('category', Validator.customer_category, category)
    return form

def validate_new_product(name, category, brand, price, mrp=None):
    """Validate all fields for a new product"""
    form = FormValidator()
    form.validate('name', Validator.name, name, min_length=2, max_length=200)
    form.validate('category', Validator.product_category, category)
    form.validate('brand', Validator.name, brand, min_length=1, max_length=100)
    form.validate('price', Validator.amount, price)
    if mrp:
        form.validate('mrp', Validator.amount, mrp)
    return form

def validate_purchase(phone, amount):
    """Validate purchase recording"""
    form = FormValidator()
    form.validate('phone', Validator.phone, phone)
    form.validate('amount', Validator.amount, amount, min_val=1)
    return form

def validate_message_send(phone, message):
    """Validate before sending a message"""
    form = FormValidator()
    form.validate('phone', Validator.phone, phone)
    form.validate('message', Validator.message_text, message)
    return form
