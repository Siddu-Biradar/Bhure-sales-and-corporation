#!/usr/bin/env python3
# ============================================================
# 🏪 BHURE ELECTRICAL - Web Dashboard (Flask)
# ============================================================
# Run: python web_app.py
# Open: http://localhost:5000
# ============================================================

import os
import sys
from datetime import datetime

sys.path.insert(0, os.path.dirname(__file__))

from flask import Flask, render_template_string, request, jsonify, redirect, url_for
from modules.customer_db import (
    add_customer, load_customers, search_customers, get_customer_stats,
    get_recent_customers, get_top_customers, get_all_active_customers,
    record_purchase, get_customer_by_phone
)
from modules.whatsapp_sender import (
    send_whatsapp_message_instantly, send_bulk_messages,
    get_message_stats, generate_whatsapp_link
)
from modules.festival_manager import (
    get_today_festivals, get_upcoming_festivals, get_festival_message,
    get_birthday_message
)
from modules.new_arrivals import add_product, get_new_arrivals, generate_new_arrival_message
from modules.bill_manager import generate_purchase_thankyou, generate_feedback_request, generate_referral_message
from modules.message_templates import (
    welcome_message, energy_saving_tips, safety_tips_monsoon, review_request
)
from modules.validators import (
    Validator, FormValidator, validate_new_customer,
    validate_new_product, validate_message_send
)

app = Flask(__name__)
SHOP_NAME = "Bhure Electrical"

# =============================================
# HTML TEMPLATE (Single-page Dashboard)
# =============================================
DASHBOARD_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ shop_name }} - Customer Engagement Dashboard</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #f0f2f5; color: #333; }
        
        /* Header */
        .header { background: linear-gradient(135deg, #075e54, #128c7e); color: white; padding: 20px 30px; display: flex; justify-content: space-between; align-items: center; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .header h1 { font-size: 24px; }
        .header .date { font-size: 14px; opacity: 0.9; }
        
        /* Navigation */
        .nav { background: #fff; padding: 10px 20px; display: flex; gap: 5px; border-bottom: 2px solid #e0e0e0; overflow-x: auto; }
        .nav button { padding: 10px 20px; border: none; background: #f0f2f5; border-radius: 20px; cursor: pointer; font-size: 14px; white-space: nowrap; transition: all 0.3s; }
        .nav button:hover, .nav button.active { background: #25d366; color: white; }
        
        /* Container */
        .container { max-width: 1200px; margin: 20px auto; padding: 0 20px; }
        
        /* Cards */
        .stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin-bottom: 20px; }
        .stat-card { background: white; border-radius: 12px; padding: 20px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); text-align: center; }
        .stat-card .number { font-size: 32px; font-weight: bold; color: #075e54; }
        .stat-card .label { font-size: 14px; color: #666; margin-top: 5px; }
        .stat-card .icon { font-size: 30px; margin-bottom: 10px; }
        
        /* Sections */
        .section { background: white; border-radius: 12px; padding: 25px; margin-bottom: 20px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); }
        .section h2 { color: #075e54; margin-bottom: 15px; font-size: 20px; }
        .section h3 { color: #333; margin-bottom: 10px; }
        
        /* Forms */
        .form-group { margin-bottom: 15px; }
        .form-group label { display: block; margin-bottom: 5px; font-weight: 600; color: #555; }
        .form-group input, .form-group select, .form-group textarea { width: 100%; padding: 10px 15px; border: 2px solid #e0e0e0; border-radius: 8px; font-size: 14px; transition: border-color 0.3s; }
        .form-group input:focus, .form-group select:focus, .form-group textarea:focus { border-color: #25d366; outline: none; }
        .form-group textarea { min-height: 120px; resize: vertical; }
        
        .form-row { display: grid; grid-template-columns: 1fr 1fr; gap: 15px; }
        @media (max-width: 600px) { .form-row { grid-template-columns: 1fr; } }
        
        /* Buttons */
        .btn { padding: 10px 25px; border: none; border-radius: 8px; cursor: pointer; font-size: 14px; font-weight: 600; transition: all 0.3s; display: inline-flex; align-items: center; gap: 8px; }
        .btn-primary { background: #25d366; color: white; }
        .btn-primary:hover { background: #1da851; }
        .btn-secondary { background: #075e54; color: white; }
        .btn-secondary:hover { background: #064e46; }
        .btn-danger { background: #e74c3c; color: white; }
        .btn-outline { background: white; color: #075e54; border: 2px solid #075e54; }
        .btn-outline:hover { background: #075e54; color: white; }
        .btn-whatsapp { background: #25d366; color: white; }
        .btn-whatsapp:hover { background: #1da851; transform: translateY(-2px); box-shadow: 0 4px 12px rgba(37,211,102,0.3); }
        
        /* Table */
        .table-container { overflow-x: auto; }
        table { width: 100%; border-collapse: collapse; }
        th, td { padding: 12px 15px; text-align: left; border-bottom: 1px solid #eee; }
        th { background: #f8f9fa; font-weight: 600; color: #555; }
        tr:hover { background: #f8fff8; }
        
        /* Alerts */
        .alert { padding: 15px 20px; border-radius: 8px; margin-bottom: 15px; display: flex; align-items: center; gap: 10px; }
        .alert-festival { background: #fff3e0; border-left: 4px solid #ff9800; }
        .alert-birthday { background: #fce4ec; border-left: 4px solid #e91e63; }
        .alert-info { background: #e3f2fd; border-left: 4px solid #2196f3; }
        .alert-success { background: #e8f5e9; border-left: 4px solid #4caf50; }
        
        /* Badge */
        .badge { padding: 4px 10px; border-radius: 12px; font-size: 12px; font-weight: 600; }
        .badge-green { background: #e8f5e9; color: #2e7d32; }
        .badge-blue { background: #e3f2fd; color: #1565c0; }
        .badge-orange { background: #fff3e0; color: #e65100; }
        .badge-red { background: #fce4ec; color: #c62828; }
        
        /* Template Cards */
        .template-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 15px; }
        .template-card { border: 2px solid #e0e0e0; border-radius: 12px; padding: 15px; cursor: pointer; transition: all 0.3s; }
        .template-card:hover { border-color: #25d366; transform: translateY(-3px); box-shadow: 0 4px 15px rgba(0,0,0,0.1); }
        .template-card h4 { color: #075e54; margin-bottom: 8px; }
        .template-card p { font-size: 13px; color: #666; }
        
        /* Tab content */
        .tab-content { display: none; }
        .tab-content.active { display: block; }
        
        /* Toast */
        .toast { position: fixed; top: 20px; right: 20px; padding: 15px 25px; border-radius: 8px; color: white; font-weight: 600; z-index: 9999; animation: slideIn 0.3s; }
        .toast-success { background: #25d366; }
        .toast-error { background: #e74c3c; }
        @keyframes slideIn { from { transform: translateX(100%); } to { transform: translateX(0); } }
        
        /* Preview Box */
        .preview-box { background: #e5ddd5; border-radius: 12px; padding: 20px; margin-top: 15px; }
        .preview-message { background: #dcf8c6; border-radius: 8px; padding: 15px; max-width: 400px; white-space: pre-wrap; font-size: 14px; line-height: 1.5; box-shadow: 0 1px 2px rgba(0,0,0,0.1); }
        
        /* Quick Actions */
        .quick-actions { display: flex; flex-wrap: wrap; gap: 10px; margin-top: 15px; }
    </style>
</head>
<body>
    <div class="header">
        <div>
            <h1>🏪 {{ shop_name }}</h1>
            <div class="date">Customer Engagement Dashboard</div>
        </div>
        <div class="date">📅 {{ today }}</div>
    </div>
    
    <div class="nav">
        <button class="active" onclick="showTab('dashboard')">📊 Dashboard</button>
        <button onclick="showTab('customers')">👥 Customers</button>
        <button onclick="showTab('messages')">📱 Send Messages</button>
        <button onclick="showTab('festivals')">🎉 Festivals</button>
        <button onclick="showTab('products')">🆕 Products</button>
        <button onclick="showTab('templates')">📨 Templates</button>
    </div>
    
    <div class="container">
        <!-- ============ DASHBOARD TAB ============ -->
        <div id="dashboard" class="tab-content active">
            <!-- Alerts -->
            {% for f in today_festivals %}
            <div class="alert alert-festival">
                <span>{{ f.emoji }}</span>
                <strong>Today is {{ f.name }}!</strong> Send festival wishes to your customers!
                <button class="btn btn-whatsapp btn-sm" onclick="showTab('festivals')" style="margin-left:auto;">Send Wishes</button>
            </div>
            {% endfor %}
            
            <!-- Stats -->
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="icon">👥</div>
                    <div class="number">{{ stats.total_customers }}</div>
                    <div class="label">Total Customers</div>
                </div>
                <div class="stat-card">
                    <div class="icon">✅</div>
                    <div class="number">{{ stats.active_customers }}</div>
                    <div class="label">Active Customers</div>
                </div>
                <div class="stat-card">
                    <div class="icon">💰</div>
                    <div class="number">₹{{ "{:,.0f}".format(stats.total_revenue) }}</div>
                    <div class="label">Total Revenue</div>
                </div>
                <div class="stat-card">
                    <div class="icon">📱</div>
                    <div class="number">{{ msg_stats.total_messages }}</div>
                    <div class="label">Messages Sent</div>
                </div>
            </div>
            
            <!-- Upcoming Events -->
            {% if upcoming_festivals %}
            <div class="section">
                <h2>📅 Upcoming Events</h2>
                {% for f in upcoming_festivals %}
                <div style="display:flex; align-items:center; gap:15px; padding:10px 0; border-bottom:1px solid #eee;">
                    <span style="font-size:24px;">{{ f.emoji }}</span>
                    <div>
                        <strong>{{ f.name }}</strong>
                        <div style="color:#666; font-size:13px;">{{ f.date }} (in {{ f.days_until }} days)</div>
                    </div>
                </div>
                {% endfor %}
            </div>
            {% endif %}
            
            <!-- Quick Actions -->
            <div class="section">
                <h2>⚡ Quick Actions</h2>
                <div class="quick-actions">
                    <button class="btn btn-whatsapp" onclick="showTab('messages')">📱 Send WhatsApp</button>
                    <button class="btn btn-secondary" onclick="showTab('customers')">➕ Add Customer</button>
                    <button class="btn btn-outline" onclick="showTab('products')">🆕 New Arrival</button>
                    <button class="btn btn-outline" onclick="showTab('templates')">📨 Templates</button>
                </div>
            </div>
        </div>
        
        <!-- ============ CUSTOMERS TAB ============ -->
        <div id="customers" class="tab-content">
            <div class="section">
                <h2>➕ Add New Customer</h2>
                <form id="addCustomerForm" onsubmit="addCustomer(event)">
                    <div class="form-row">
                        <div class="form-group">
                            <label>Name *</label>
                            <input type="text" id="c_name" required placeholder="Customer name">
                        </div>
                        <div class="form-group">
                            <label>Phone *</label>
                            <input type="text" id="c_phone" required placeholder="10-digit mobile number">
                        </div>
                    </div>
                    <div class="form-row">
                        <div class="form-group">
                            <label>Email</label>
                            <input type="email" id="c_email" placeholder="Email (optional)">
                        </div>
                        <div class="form-group">
                            <label>Category</label>
                            <select id="c_category">
                                <option>General</option>
                                <option>Regular</option>
                                <option>VIP</option>
                                <option>Electrician</option>
                                <option>Contractor</option>
                                <option>Builder</option>
                            </select>
                        </div>
                    </div>
                    <div class="form-row">
                        <div class="form-group">
                            <label>Birthday</label>
                            <input type="date" id="c_birthday">
                        </div>
                        <div class="form-group">
                            <label>Anniversary</label>
                            <input type="date" id="c_anniversary">
                        </div>
                    </div>
                    <div class="form-group">
                        <label>Address</label>
                        <input type="text" id="c_address" placeholder="Address (optional)">
                    </div>
                    <button type="submit" class="btn btn-primary">➕ Add Customer</button>
                </form>
            </div>
            
            <div class="section">
                <h2>👥 Customer List</h2>
                <div class="form-group">
                    <input type="text" id="searchInput" placeholder="🔍 Search by name or phone..." oninput="filterCustomers()">
                </div>
                <div class="table-container">
                    <table id="customerTable">
                        <thead>
                            <tr>
                                <th>ID</th>
                                <th>Name</th>
                                <th>Phone</th>
                                <th>Category</th>
                                <th>Total Spent</th>
                                <th>Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for _, c in customers.iterrows() %}
                            <tr>
                                <td>{{ c.customer_id }}</td>
                                <td><strong>{{ c.name }}</strong></td>
                                <td>{{ c.phone }}</td>
                                <td><span class="badge badge-green">{{ c.category }}</span></td>
                                <td>₹{{ "{:,.0f}".format(c.total_amount_spent or 0) }}</td>
                                <td>
                                    <button class="btn btn-whatsapp" style="padding:5px 12px; font-size:12px;" onclick="openWhatsApp('{{ c.phone }}', '{{ c.name }}')">📱 WhatsApp</button>
                                </td>
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
        
        <!-- ============ MESSAGES TAB ============ -->
        <div id="messages" class="tab-content">
            <div class="section">
                <h2>📱 Send WhatsApp Message</h2>
                <div class="form-group">
                    <label>Send To</label>
                    <select id="msg_target" onchange="updateRecipients()">
                        <option value="single">Single Customer</option>
                        <option value="all">All Customers</option>
                        <option value="category">By Category</option>
                        <option value="recent">Recent Customers (30 days)</option>
                    </select>
                </div>
                <div class="form-group" id="single_phone_group">
                    <label>Phone Number</label>
                    <input type="text" id="msg_phone" placeholder="+919876543210">
                </div>
                <div class="form-group" id="category_group" style="display:none;">
                    <label>Category</label>
                    <select id="msg_category">
                        <option>General</option>
                        <option>Regular</option>
                        <option>VIP</option>
                        <option>Electrician</option>
                        <option>Contractor</option>
                    </select>
                </div>
                <div class="form-group">
                    <label>Message</label>
                    <textarea id="msg_text" placeholder="Type your message here... Use * for bold in WhatsApp"></textarea>
                </div>
                
                <!-- Preview -->
                <div class="preview-box">
                    <strong>📱 Preview:</strong>
                    <div class="preview-message" id="msgPreview">Your message will appear here...</div>
                </div>
                
                <div style="margin-top:15px; display:flex; gap:10px;">
                    <button class="btn btn-whatsapp" onclick="sendMessage()">📤 Send via WhatsApp</button>
                    <button class="btn btn-outline" onclick="generateLink()">🔗 Generate Link</button>
                </div>
                <div id="waLink" style="margin-top:10px; display:none;">
                    <input type="text" id="waLinkInput" readonly style="width:100%; padding:10px; background:#f5f5f5; border:1px solid #ddd; border-radius:8px;">
                </div>
            </div>
        </div>
        
        <!-- ============ FESTIVALS TAB ============ -->
        <div id="festivals" class="tab-content">
            {% if today_festivals %}
            <div class="section" style="background: linear-gradient(135deg, #fff3e0, #ffe0b2);">
                <h2>🎉 Today's Festivals</h2>
                {% for f in today_festivals %}
                <div class="alert alert-festival">
                    <span style="font-size:28px;">{{ f.emoji }}</span>
                    <div>
                        <strong style="font-size:18px;">{{ f.name }}</strong>
                        <p>Send wishes to all your customers!</p>
                    </div>
                    <button class="btn btn-whatsapp" style="margin-left:auto;" onclick="sendFestivalWishes('{{ f.name }}')">🎉 Send Wishes to All</button>
                </div>
                {% endfor %}
            </div>
            {% endif %}
            
            <div class="section">
                <h2>📅 Upcoming Events (Next 30 Days)</h2>
                {% for f in upcoming_30 %}
                <div style="display:flex; align-items:center; gap:15px; padding:12px 0; border-bottom:1px solid #eee;">
                    <span style="font-size:28px;">{{ f.emoji }}</span>
                    <div style="flex:1;">
                        <strong>{{ f.name }}</strong>
                        <div style="color:#666; font-size:13px;">{{ f.date }} &mdash; {{ f.days_until }} days from now</div>
                    </div>
                    <span class="badge badge-orange">{{ f.type }}</span>
                </div>
                {% endfor %}
                {% if not upcoming_30 %}
                <p>No upcoming events in the next 30 days.</p>
                {% endif %}
            </div>
        </div>
        
        <!-- ============ PRODUCTS TAB ============ -->
        <div id="products" class="tab-content">
            <div class="section">
                <h2>➕ Add New Product</h2>
                <form onsubmit="addProduct(event)">
                    <div class="form-row">
                        <div class="form-group">
                            <label>Product Name *</label>
                            <input type="text" id="p_name" required placeholder="e.g., Havells 1200mm Ceiling Fan">
                        </div>
                        <div class="form-group">
                            <label>Brand *</label>
                            <input type="text" id="p_brand" required placeholder="e.g., Havells, Crompton">
                        </div>
                    </div>
                    <div class="form-row">
                        <div class="form-group">
                            <label>Category</label>
                            <select id="p_category">
                                <option>LED Lights</option>
                                <option>Ceiling Fans</option>
                                <option>Table Fans</option>
                                <option>Switches & Sockets</option>
                                <option>Wires & Cables</option>
                                <option>Inverters & UPS</option>
                                <option>Water Heaters</option>
                                <option>Decorative Lights</option>
                                <option>MCBs & Distribution Boards</option>
                                <option>Extension Boards</option>
                                <option>Solar Products</option>
                                <option>CCTV & Security</option>
                            </select>
                        </div>
                        <div class="form-group">
                            <label>Selling Price (₹) *</label>
                            <input type="number" id="p_price" required placeholder="1299">
                        </div>
                    </div>
                    <div class="form-group">
                        <label>MRP (₹)</label>
                        <input type="number" id="p_mrp" placeholder="1599 (optional)">
                    </div>
                    <button type="submit" class="btn btn-primary">➕ Add Product</button>
                </form>
            </div>
            
            <div class="section">
                <h2>🆕 New Arrivals</h2>
                {% if new_arrivals %}
                <div class="table-container">
                    <table>
                        <thead><tr><th>ID</th><th>Product</th><th>Brand</th><th>Category</th><th>Price</th><th>MRP</th></tr></thead>
                        <tbody>
                            {% for p in new_arrivals %}
                            <tr>
                                <td>{{ p.id }}</td>
                                <td><strong>{{ p.name }}</strong></td>
                                <td>{{ p.brand }}</td>
                                <td>{{ p.category }}</td>
                                <td>₹{{ "{:,}".format(p.price|int) }}</td>
                                <td>{% if p.mrp > p.price %}<s>₹{{ "{:,}".format(p.mrp|int) }}</s>{% else %}-{% endif %}</td>
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
                <button class="btn btn-whatsapp" style="margin-top:15px;" onclick="sendNewArrivals()">📤 Announce to All Customers</button>
                {% else %}
                <p>No products added yet. Add your first product above!</p>
                {% endif %}
            </div>
        </div>
        
        <!-- ============ TEMPLATES TAB ============ -->
        <div id="templates" class="tab-content">
            <div class="section">
                <h2>📨 Ready-to-Use Message Templates</h2>
                <p style="color:#666; margin-bottom:15px;">Click on any template to preview and send!</p>
                <div class="template-grid">
                    <div class="template-card" onclick="loadTemplate('welcome')">
                        <h4>👋 Welcome Message</h4>
                        <p>Send to new customers after their first visit</p>
                    </div>
                    <div class="template-card" onclick="loadTemplate('energy_tips')">
                        <h4>💡 Energy Saving Tips</h4>
                        <p>Useful tips that keep customers engaged</p>
                    </div>
                    <div class="template-card" onclick="loadTemplate('monsoon_safety')">
                        <h4>⚡ Monsoon Safety Tips</h4>
                        <p>Seasonal electrical safety awareness</p>
                    </div>
                    <div class="template-card" onclick="loadTemplate('feedback')">
                        <h4>⭐ Feedback Request</h4>
                        <p>Ask recent customers for their feedback</p>
                    </div>
                    <div class="template-card" onclick="loadTemplate('referral')">
                        <h4>🎁 Referral Program</h4>
                        <p>Encourage customers to refer friends</p>
                    </div>
                    <div class="template-card" onclick="loadTemplate('review')">
                        <h4>⭐ Google Review</h4>
                        <p>Request Google Maps reviews</p>
                    </div>
                    <div class="template-card" onclick="loadTemplate('emi')">
                        <h4>💳 EMI Available</h4>
                        <p>Inform about EMI/finance options</p>
                    </div>
                    <div class="template-card" onclick="loadTemplate('win_back')">
                        <h4>👋 Win-Back Message</h4>
                        <p>Re-engage inactive customers</p>
                    </div>
                </div>
            </div>
            
            <div class="section" id="templatePreview" style="display:none;">
                <h2>📝 Template Preview</h2>
                <div class="preview-box">
                    <div class="preview-message" id="templateContent"></div>
                </div>
                <div style="margin-top:15px; display:flex; gap:10px;">
                    <button class="btn btn-whatsapp" onclick="useTemplate()">📤 Send to All Customers</button>
                    <button class="btn btn-outline" onclick="copyTemplate()">📋 Copy Message</button>
                </div>
            </div>
        </div>
    </div>
    
    <div id="toast" class="toast" style="display:none;"></div>
    
    <script>
        // Tab Navigation
        function showTab(tabId) {
            document.querySelectorAll('.tab-content').forEach(t => t.classList.remove('active'));
            document.querySelectorAll('.nav button').forEach(b => b.classList.remove('active'));
            document.getElementById(tabId).classList.add('active');
            event.target.classList.add('active');
        }
        
        // Toast notifications
        function showToast(message, type='success') {
            const toast = document.getElementById('toast');
            toast.textContent = message;
            toast.className = 'toast toast-' + type;
            toast.style.display = 'block';
            setTimeout(() => toast.style.display = 'none', 3000);
        }
        
        // Message preview
        document.getElementById('msg_text')?.addEventListener('input', function() {
            document.getElementById('msgPreview').textContent = this.value || 'Your message will appear here...';
        });
        
        // Add Customer
        async function addCustomer(e) {
            e.preventDefault();
            const data = {
                name: document.getElementById('c_name').value,
                phone: document.getElementById('c_phone').value,
                email: document.getElementById('c_email').value,
                category: document.getElementById('c_category').value,
                birthday: document.getElementById('c_birthday').value,
                anniversary: document.getElementById('c_anniversary').value,
                address: document.getElementById('c_address').value,
            };
            
            const res = await fetch('/api/customer/add', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(data)
            });
            const result = await res.json();
            
            if (result.success) {
                showToast('✅ ' + result.message);
                location.reload();
            } else {
                showToast('❌ ' + result.message, 'error');
            }
        }
        
        // Add Product
        async function addProduct(e) {
            e.preventDefault();
            const data = {
                name: document.getElementById('p_name').value,
                brand: document.getElementById('p_brand').value,
                category: document.getElementById('p_category').value,
                price: parseFloat(document.getElementById('p_price').value),
                mrp: parseFloat(document.getElementById('p_mrp').value) || 0,
            };
            
            const res = await fetch('/api/product/add', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(data)
            });
            const result = await res.json();
            showToast(result.success ? '✅ Product added!' : '❌ Failed', result.success ? 'success' : 'error');
            if (result.success) location.reload();
        }
        
        // Send Message
        async function sendMessage() {
            const target = document.getElementById('msg_target').value;
            const message = document.getElementById('msg_text').value;
            
            if (!message) { showToast('Please enter a message!', 'error'); return; }
            
            const data = { target, message };
            if (target === 'single') data.phone = document.getElementById('msg_phone').value;
            if (target === 'category') data.category = document.getElementById('msg_category').value;
            
            showToast('📤 Sending messages...');
            const res = await fetch('/api/message/send', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(data)
            });
            const result = await res.json();
            showToast(result.message, result.success ? 'success' : 'error');
        }
        
        // Generate WhatsApp Link
        function generateLink() {
            const phone = document.getElementById('msg_phone').value;
            const message = document.getElementById('msg_text').value;
            if (!phone || !message) { showToast('Enter phone and message!', 'error'); return; }
            
            const cleanPhone = phone.replace(/[^0-9]/g, '');
            const link = `https://wa.me/${cleanPhone}?text=${encodeURIComponent(message)}`;
            document.getElementById('waLinkInput').value = link;
            document.getElementById('waLink').style.display = 'block';
            
            // Also open in new tab
            window.open(link, '_blank');
        }
        
        // Open WhatsApp for a customer
        function openWhatsApp(phone, name) {
            const message = `Hello ${name} ji! This is from Bhure Electrical. `;
            const cleanPhone = phone.replace(/[^0-9]/g, '');
            window.open(`https://wa.me/${cleanPhone}?text=${encodeURIComponent(message)}`, '_blank');
        }
        
        // Send Festival Wishes
        async function sendFestivalWishes(festivalName) {
            if (!confirm(`Send ${festivalName} wishes to ALL customers?`)) return;
            showToast('🎉 Sending festival wishes...');
            const res = await fetch('/api/festival/send', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ festival: festivalName })
            });
            const result = await res.json();
            showToast(result.message, result.success ? 'success' : 'error');
        }
        
        // Send New Arrivals
        async function sendNewArrivals() {
            if (!confirm('Announce new arrivals to ALL customers?')) return;
            showToast('📤 Sending new arrival announcements...');
            const res = await fetch('/api/arrivals/send', { method: 'POST' });
            const result = await res.json();
            showToast(result.message, result.success ? 'success' : 'error');
        }
        
        // Template Loading
        const templates = {
            'welcome': `👋 Welcome to Bhure Electrical!\\n\\nThank you for visiting us! We are your one-stop shop for all electrical needs.\\n\\n💡 LED Lights  ⚡ Fans  🔌 Switches  🔋 Inverters\\n\\n✅ Branded products at best prices\\n✅ Expert advice\\n✅ Home delivery available\\n\\nSave this number for quick orders & offers!\\n~ Team Bhure Electrical`,
            'energy_tips': `💡 Energy Saving Tips by Bhure Electrical!\\n\\n1️⃣ Switch to LED lights - save 80% power\\n2️⃣ Use 5-star rated appliances\\n3️⃣ Turn off when not in use\\n4️⃣ Use timer switches\\n5️⃣ Set AC to 24°C\\n\\nVisit us for energy-efficient products!\\n~ Team Bhure Electrical`,
            'monsoon_safety': `⚡ Monsoon Safety Tips by Bhure Electrical!\\n\\n1️⃣ Check connections for water leakage\\n2️⃣ Use MCB/ELCB for safety\\n3️⃣ Avoid damaged switches\\n4️⃣ Keep appliances away from water\\n5️⃣ Use waterproof fittings outdoors\\n\\nVisit us for safety products!\\n~ Team Bhure Electrical`,
            'feedback': `⭐ We Value Your Feedback!\\n\\nDear Customer,\\n\\nThank you for shopping at Bhure Electrical!\\n\\n1️⃣ How was our service?\\n2️⃣ Did you find what you needed?\\n3️⃣ Any suggestions?\\n\\nReply to share your feedback!\\n~ Team Bhure Electrical`,
            'referral': `🎁 REFER & EARN at Bhure Electrical!\\n\\nRefer a friend → They make a purchase → You BOTH get 5% OFF!\\n\\nShare Bhure Electrical with your loved ones and save together!\\n~ Team Bhure Electrical`,
            'review': `⭐ Rate Us on Google!\\n\\nIf you're happy with our products & service, please leave us a Google Review!\\n\\nYour review helps us grow!\\n~ Team Bhure Electrical`,
            'emi': `💳 EMI Now Available at Bhure Electrical!\\n\\n✅ 0% interest on select items\\n✅ 3/6/9/12 month EMI\\n✅ All credit cards accepted\\n✅ Bajaj Finserv EMI card\\n\\nBuy Inverters, Fans, Lights on Easy EMI!\\n~ Team Bhure Electrical`,
            'win_back': `👋 We Miss You at Bhure Electrical!\\n\\nIt's been a while! We have new products & exciting offers!\\n\\n🆕 New arrivals every week\\n🏷️ Special comeback discount - 10% OFF!\\n\\nVisit us today! Show this message for the offer.\\n~ Team Bhure Electrical`
        };
        
        function loadTemplate(key) {
            document.getElementById('templatePreview').style.display = 'block';
            document.getElementById('templateContent').textContent = templates[key].replace(/\\n/g, '\\n');
            document.getElementById('templatePreview').scrollIntoView({ behavior: 'smooth' });
        }
        
        function useTemplate() {
            const msg = document.getElementById('templateContent').textContent;
            document.getElementById('msg_text').value = msg;
            showTab('messages');
            document.querySelector('.nav button:nth-child(3)').classList.add('active');
        }
        
        function copyTemplate() {
            const msg = document.getElementById('templateContent').textContent;
            navigator.clipboard.writeText(msg).then(() => showToast('📋 Copied to clipboard!'));
        }
        
        // Update recipients UI
        function updateRecipients() {
            const target = document.getElementById('msg_target').value;
            document.getElementById('single_phone_group').style.display = target === 'single' ? 'block' : 'none';
            document.getElementById('category_group').style.display = target === 'category' ? 'block' : 'none';
        }
        
        // Filter customers table
        function filterCustomers() {
            const query = document.getElementById('searchInput').value.toLowerCase();
            const rows = document.querySelectorAll('#customerTable tbody tr');
            rows.forEach(row => {
                const text = row.textContent.toLowerCase();
                row.style.display = text.includes(query) ? '' : 'none';
            });
        }
    </script>
</body>
</html>
"""

# =============================================
# ROUTES
# =============================================
@app.route('/')
def index():
    customers = load_customers()
    stats = get_customer_stats()
    msg_stats = get_message_stats()
    today_festivals = get_today_festivals()
    upcoming = get_upcoming_festivals(7)
    upcoming_30 = get_upcoming_festivals(30)
    new_arrivals = get_new_arrivals(10)
    
    return render_template_string(DASHBOARD_HTML,
        shop_name=SHOP_NAME,
        today=datetime.now().strftime('%d %B %Y, %A'),
        customers=customers,
        stats=stats,
        msg_stats=msg_stats,
        today_festivals=today_festivals,
        upcoming_festivals=upcoming,
        upcoming_30=upcoming_30,
        new_arrivals=new_arrivals
    )

@app.route('/api/customer/add', methods=['POST'])
def api_add_customer():
    data = request.json
    
    # Validate inputs
    form = validate_new_customer(
        name=data.get('name', ''),
        phone=data.get('phone', ''),
        email=data.get('email', ''),
        birthday=data.get('birthday', ''),
        category=data.get('category', 'General')
    )
    if not form.is_valid:
        return jsonify({'success': False, 'message': form.get_error_summary(), 'errors': form.get_errors_dict()})
    
    success, message = add_customer(
        name=form.cleaned.get('name', data.get('name', '')),
        phone=form.cleaned.get('phone', data.get('phone', '')),
        email=form.cleaned.get('email', data.get('email', '')),
        address=data.get('address', ''),
        birthday=form.cleaned.get('birthday', data.get('birthday', '')),
        anniversary=data.get('anniversary', ''),
        category=form.cleaned.get('category', 'General')
    )
    return jsonify({'success': success, 'message': message})

@app.route('/api/product/add', methods=['POST'])
def api_add_product():
    data = request.json
    
    # Validate inputs
    form = validate_new_product(
        name=data.get('name', ''),
        category=data.get('category', ''),
        brand=data.get('brand', ''),
        price=data.get('price', 0),
        mrp=data.get('mrp', 0) if data.get('mrp') else None
    )
    if not form.is_valid:
        return jsonify({'success': False, 'message': form.get_error_summary(), 'errors': form.get_errors_dict()})
    
    success, message = add_product(
        name=form.cleaned.get('name', data.get('name', '')),
        category=form.cleaned.get('category', data.get('category', '')),
        brand=form.cleaned.get('brand', data.get('brand', '')),
        price=form.cleaned.get('price', data.get('price', 0)),
        mrp=form.cleaned.get('mrp', data.get('mrp', 0))
    )
    return jsonify({'success': success, 'message': message})

@app.route('/api/message/send', methods=['POST'])
def api_send_message():
    data = request.json
    target = data.get('target', 'single')
    message = data.get('message', '')
    
    # Validate message text
    msg_valid, msg_result = Validator.message_text(message)
    if not msg_valid:
        return jsonify({'success': False, 'message': f'Message error: {msg_result}'})
    
    if target == 'single':
        phone = data.get('phone', '')
        # Validate phone
        phone_valid, phone_result = Validator.phone(phone)
        if not phone_valid:
            return jsonify({'success': False, 'message': f'Phone error: {phone_result}'})
        success, msg = send_whatsapp_message_instantly(phone_result, message)
        return jsonify({'success': success, 'message': msg})
    
    elif target == 'all':
        customers = get_all_active_customers()
        if customers.empty:
            return jsonify({'success': False, 'message': 'No customers!'})
        results = send_bulk_messages(customers['phone'].tolist(), message)
        return jsonify({'success': True, 'message': f"Sent: {results['sent']}, Failed: {results['failed']}"})
    
    elif target == 'category':
        category = data.get('category', 'General')
        customers = load_customers()
        filtered = customers[customers['category'] == category]
        if filtered.empty:
            return jsonify({'success': False, 'message': f'No customers in {category}!'})
        results = send_bulk_messages(filtered['phone'].tolist(), message)
        return jsonify({'success': True, 'message': f"Sent: {results['sent']}, Failed: {results['failed']}"})
    
    elif target == 'recent':
        recent = get_recent_customers(30)
        if recent.empty:
            return jsonify({'success': False, 'message': 'No recent customers!'})
        results = send_bulk_messages(recent['phone'].tolist(), message)
        return jsonify({'success': True, 'message': f"Sent: {results['sent']}, Failed: {results['failed']}"})
    
    return jsonify({'success': False, 'message': 'Invalid target'})

@app.route('/api/festival/send', methods=['POST'])
def api_send_festival():
    try:
        data = request.json
        festival_name = data.get('festival', '')
        customers = get_all_active_customers()
        
        if customers.empty:
            return jsonify({'success': False, 'message': 'No customers!'})
        
        messages = []
        for _, c in customers.iterrows():
            msg = get_festival_message(festival_name, c['name'], SHOP_NAME)
            messages.append((c['phone'], msg))
        
        results = send_personalized_messages(messages)
        return jsonify({
            'success': True, 
            'message': f"🎉 Festival wishes sent! ✅ {results['sent']} sent, ❌ {results['failed']} failed"
        })
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'})

@app.route('/api/arrivals/send', methods=['POST'])
def api_send_arrivals():
    arrivals = get_new_arrivals(5)
    customers = get_all_active_customers()
    
    if customers.empty:
        return jsonify({'success': False, 'message': 'No customers!'})
    if not arrivals:
        return jsonify({'success': False, 'message': 'No new arrivals!'})
    
    messages = []
    for _, c in customers.iterrows():
        msg = generate_new_arrival_message(arrivals, c['name'], SHOP_NAME)
        messages.append((c['phone'], msg))
    
    from modules.whatsapp_sender import send_personalized_messages
    results = send_personalized_messages(messages)
    return jsonify({
        'success': True,
        'message': f"📤 Announcements sent! ✅ {results['sent']} sent, ❌ {results['failed']} failed"
    })

if __name__ == '__main__':
    print(f"\n  🏪 {SHOP_NAME} - Web Dashboard")
    print(f"  {'─' * 40}")
    print(f"  🌐 Open: http://localhost:5001")
    print(f"  Press Ctrl+C to stop\n")
    app.run(debug=True, port=5001)
