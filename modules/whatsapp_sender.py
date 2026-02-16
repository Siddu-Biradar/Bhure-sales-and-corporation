# ============================================
# Bhure Electrical - WhatsApp Messaging Module
# ============================================
# Handles sending messages via WhatsApp Web using pywhatkit

import pywhatkit as kit
import time
import os
import json
import logging
from datetime import datetime

# Setup logging
LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')
os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(
    filename=os.path.join(LOG_DIR, f'messages_{datetime.now().strftime("%Y%m%d")}.log'),
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Message log file
MESSAGE_LOG = os.path.join(LOG_DIR, 'message_history.json')

def load_message_history():
    """Load message sending history"""
    if os.path.exists(MESSAGE_LOG):
        with open(MESSAGE_LOG, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_message_log(log_entry):
    """Save a message log entry"""
    history = load_message_history()
    history.append(log_entry)
    with open(MESSAGE_LOG, 'w', encoding='utf-8') as f:
        json.dump(history, f, indent=2, ensure_ascii=False)

def send_whatsapp_message(phone, message, wait_time=15):
    """
    Send a WhatsApp message to a single number.
    
    IMPORTANT: WhatsApp Web must be logged in on your default browser!
    
    Args:
        phone: Phone number with country code (e.g., +919876543210)
        message: Message text to send
        wait_time: Seconds to wait for WhatsApp Web to load
    
    Returns:
        (success: bool, message: str)
    """
    try:
        phone = str(phone).strip()
        if not phone.startswith('+'):
            phone = '+91' + phone.lstrip('0')
        
        now = datetime.now()
        hour = now.hour
        minute = now.minute + 2  # Send 2 minutes from now
        
        if minute >= 60:
            hour += 1
            minute -= 60
        
        logging.info(f"Sending message to {phone}")
        
        kit.sendwhatmsg(
            phone_no=phone,
            message=message,
            time_hour=hour,
            time_min=minute,
            wait_time=wait_time,
            tab_close=True
        )
        
        # Log success
        log_entry = {
            'phone': phone,
            'message_preview': message[:100] + '...' if len(message) > 100 else message,
            'status': 'sent',
            'timestamp': now.strftime('%Y-%m-%d %H:%M:%S'),
            'type': 'individual'
        }
        save_message_log(log_entry)
        
        logging.info(f"Message sent successfully to {phone}")
        return True, "Message sent successfully!"
        
    except Exception as e:
        logging.error(f"Failed to send message to {phone}: {str(e)}")
        log_entry = {
            'phone': phone,
            'message_preview': message[:100],
            'status': 'failed',
            'error': str(e),
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'type': 'individual'
        }
        save_message_log(log_entry)
        return False, f"Failed: {str(e)}"

def send_whatsapp_message_instantly(phone, message):
    """
    Send a WhatsApp message instantly (faster method).
    Uses pywhatkit's instant send feature.
    """
    try:
        phone = str(phone).strip()
        if not phone.startswith('+'):
            phone = '+91' + phone.lstrip('0')
        
        kit.sendwhatmsg_instantly(
            phone_no=phone,
            message=message,
            wait_time=12,
            tab_close=True
        )
        
        log_entry = {
            'phone': phone,
            'message_preview': message[:100],
            'status': 'sent',
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'type': 'instant'
        }
        save_message_log(log_entry)
        
        return True, "Message sent!"
    except Exception as e:
        logging.error(f"Instant send failed to {phone}: {str(e)}")
        return False, f"Failed: {str(e)}"

def send_bulk_messages(phone_list, message, delay_seconds=10):
    """
    Send same message to multiple customers.
    
    Args:
        phone_list: List of phone numbers
        message: Message to send to all
        delay_seconds: Delay between each message (to avoid spam detection)
    
    Returns:
        dict with success/failure counts
    """
    results = {
        'total': len(phone_list),
        'sent': 0,
        'failed': 0,
        'details': []
    }
    
    for i, phone in enumerate(phone_list):
        print(f"  Sending {i+1}/{len(phone_list)} to {phone}...")
        success, msg = send_whatsapp_message_instantly(phone, message)
        
        if success:
            results['sent'] += 1
        else:
            results['failed'] += 1
        
        results['details'].append({
            'phone': phone,
            'status': 'sent' if success else 'failed',
            'message': msg
        })
        
        # Delay between messages to avoid being flagged
        if i < len(phone_list) - 1:
            print(f"  Waiting {delay_seconds} seconds before next message...")
            time.sleep(delay_seconds)
    
    # Log bulk send
    log_entry = {
        'type': 'bulk',
        'total': results['total'],
        'sent': results['sent'],
        'failed': results['failed'],
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'message_preview': message[:100]
    }
    save_message_log(log_entry)
    
    return results

def send_personalized_messages(customer_message_list, delay_seconds=10):
    """
    Send personalized messages to multiple customers.
    
    Args:
        customer_message_list: List of tuples [(phone, personalized_message), ...]
        delay_seconds: Delay between messages
    
    Returns:
        dict with results
    """
    results = {
        'total': len(customer_message_list),
        'sent': 0,
        'failed': 0,
        'details': []
    }
    
    for i, (phone, message) in enumerate(customer_message_list):
        print(f"  Sending personalized msg {i+1}/{len(customer_message_list)} to {phone}...")
        success, msg = send_whatsapp_message_instantly(phone, message)
        
        if success:
            results['sent'] += 1
        else:
            results['failed'] += 1
        
        results['details'].append({
            'phone': phone,
            'status': 'sent' if success else 'failed'
        })
        
        if i < len(customer_message_list) - 1:
            time.sleep(delay_seconds)
    
    return results

def send_image_message(phone, image_path, caption=''):
    """Send an image via WhatsApp"""
    try:
        phone = str(phone).strip()
        if not phone.startswith('+'):
            phone = '+91' + phone.lstrip('0')
        
        kit.sendwhats_image(
            receiver=phone,
            img_path=image_path,
            caption=caption,
            wait_time=15,
            tab_close=True
        )
        
        log_entry = {
            'phone': phone,
            'type': 'image',
            'caption': caption[:50],
            'status': 'sent',
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        save_message_log(log_entry)
        
        return True, "Image sent!"
    except Exception as e:
        logging.error(f"Image send failed to {phone}: {str(e)}")
        return False, f"Failed: {str(e)}"

def get_message_stats():
    """Get messaging statistics"""
    history = load_message_history()
    if not history:
        return {
            'total_messages': 0,
            'sent': 0,
            'failed': 0,
            'today': 0
        }
    
    today = datetime.now().strftime('%Y-%m-%d')
    today_msgs = [h for h in history if h.get('timestamp', '').startswith(today)]
    sent = len([h for h in history if h.get('status') == 'sent'])
    failed = len([h for h in history if h.get('status') == 'failed'])
    
    return {
        'total_messages': len(history),
        'sent': sent,
        'failed': failed,
        'today': len(today_msgs)
    }

def generate_whatsapp_link(phone, message):
    """Generate a WhatsApp click-to-chat link (useful for manual sending)"""
    import urllib.parse
    phone = str(phone).strip().replace('+', '')
    encoded_msg = urllib.parse.quote(message)
    return f"https://wa.me/{phone}?text={encoded_msg}"
