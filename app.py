import os
import json
from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from paystackapi.paystack import Paystack

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'your-secret-key')

# Paystack configuration
paystack_secret_key = os.getenv('PAYSTACK_SECRET_KEY', 'your-paystack-secret-key')
paystack = Paystack(secret_key=paystack_secret_key)

# Manual product catalog with options
products = {
    "Clothes": [
        {"id": 1, "name": "Trendy Offwhite Up And Down Wears", "price": 20000.00, "image": "/static/c1.jpg", "options": ["S", "M", "L", "XL", "XXL", "XXXL"]},
        {"id": 2, "name": "Custom-Made Trendy Up And Down Wears 2", "price": 20000.00, "image": "/static/c2.jpg", "options": ["S", "M", "L", "XL", "XXL", "XXXL"]},
        {"id": 3, "name": "Trendy Blue Up And Down Wears Pk2", "price": 20000.00, "image": "/static/c3.jpg", "options": ["S", "M", "L", "XL", "XXL", "XXXL"]},
        {"id": 4, "name": "4 IN 1 UNISEX COLLAR N PLAIN ROUND NECK T-SHIRT POLO SHIRT FOR MEN", "price": 25000.00, "image": "/static/c4.jpg", "options": ["S", "M", "L", "XL", "XXL", "XXXL"]},
        {"id": 5, "name": "Men`s 3 In 1 Sleeveless Hoodie T-Shirts For Gym & Sport - Multi", "price": 20000.00, "image": "/static/c5.jpg", "options": ["S", "M", "L", "XL", "XXL", "XXXL"]},
        {"id": 6, "name": "2 In 1 Classic Mens Formal Fit Shirts - Black And Wine", "price": 16000.00, "image": "/static/c6.jpg", "options": ["S", "M", "L", "XL"]},
        {"id": 7, "name": "Kingskartel Kings Kartel Tank Top/Sleeveless 4 In One Combo", "price": 22999.00, "image": "/static/c7.jpg", "options": ["S", "M", "L", "XL"]},
        {"id": 8, "name": "Black And Green Corduroy T-Shirt", "price": 18000.00, "image": "/static/c8.jpg", "options": ["S", "M", "L", "XL"]},
        {"id": 9, "name": "Green With Patch Brown Corduroy T-shirt", "price": 18000.00, "image": "/static/c9.jpg", "options": ["S", "M", "L", "XL"]},
        {"id": 10, "name": "3 In 1 Casual Straight Cut Joggers Pants -Dark Grey/Black/ Light Grey", "price": 36999.00, "image": "/static/c10.jpg", "options": ["S", "M", "L", "XL"]}
    ],
    "Shoes": [
        {"id": 11, "name": "Men'S Lightweight Shoes - Casual Athletic Sneakers - Black Canvas", "price": 8999.00, "image": "/static/s1.jpg", "options": ["EU 40", "EU 41", "EU 43", "EU 44"]},
        {"id": 12, "name": "DEPALLY ROUND STONE DESIGNERS SHOE BLACK", "price": 28980.00, "image": "/static/s2.jpg", "options": ["EU 40", "EU 41", "EU 42", "EU 43", "EU 44", "EU 45"]},
        {"id": 13, "name": "Men'S Trendy Men's Outdoor Sport Lace-up Casual Comfortable Sneakers - Canvas - Size", "price": 20000.00, "image": "/static/s3.jpg", "options": ["EU 43", "EU 44"]},
        {"id": 14, "name": "Men'S Men Fashion Quality Outdoor comfortable Casual Shoes", "price": 20999.00, "image": "/static/s4.jpg", "options": ["EU 43", "EU 44"]},
        {"id": 15, "name": "Canvas Men's Casual Simple Sport Fashion Sneakers - Comfortable Shoes", "price": 8980.00, "image": "/static/s5.jpg", "options": ["EU 39", "EU 40", "EU 44"]},
        {"id": 16, "name": "Men Leather Shoes Oxford Wedding Corporate Formal Loafers Slip-Ons Vintage Brown", "price": 29500.00, "image": "/static/s6.jpg", "options": ["EU 40", "EU 41", "EU 42", "EU 43", "EU 44", "EU 45"]},
        {"id": 17, "name": "Depally Men's Brogue Tie Designers Shoe Black", "price": 32000.00, "image": "/static/s7.jpg", "options": ["EU 40", "EU 41", "EU 42", "EU 43", "EU 44", "EU 45"]},
        {"id": 18, "name": "Men's Leather Shoes Large Size-Black", "price": 16980.00, "image": "/static/s8.jpg", "options": ["EU 40", "EU 41", "EU 42", "EU 43", "EU 44", "EU 45"]},
        {"id": 19, "name": "Men's Formal Italian Wedding Brogues Leather Shoes Lace Up Brown", "price": 27900.00, "image": "/static/s9.jpg", "options": ["EU 40", "EU 41", "EU 42", "EU 43", "EU 44", "EU 45"]},
        {"id": 20, "name": "Men'S 2024 Men's Casual Simple Board Sport Running Shoes - Fashion Outdoor Shoes", "price": 8999.00, "image": "/static/s10.jpg", "options": ["EU 40", "EU 41", "EU 42", "EU 43", "EU 44", "EU 45"]},
        {"id": 21, "name": "Men's All-match Leather Shoes", "price": 30499.00, "image": "/static/s11.jpg", "options": ["EU 40", "EU 41", "EU 42", "EU 43", "EU 44", "EU 45"]},
        {"id": 22, "name": "Lit Men's Fashion Sports Outdoor Running Sneakers - Sports Shoes", "price": 20999.00, "image": "/static/s12.jpg", "options": ["EU 40", "EU 41", "EU 42", "EU 43", "EU 44", "EU 45"]},
        {"id": 23, "name": "2021 New Men's Damping Running Shoes Breathable Sneaker", "price": 52084.00, "image": "/static/s13.jpg", "options": ["EU 40", "EU 41", "EU 42", "EU 43", "EU 44", "EU 45"]},
        {"id": 24, "name": "ElegantMen's Half Shoe", "price": 28980.00, "image": "/static/s14.jpg", "options": ["EU 40", "EU 41", "EU 42", "EU 43", "EU 44", "EU 45"]},
        {"id": 25, "name": "Executive Business Men Leather Loafer Shoes- Black", "price": 6999.00, "image": "/static/s15.jpg", "options": ["EU 40", "EU 41", "EU 42", "EU 43", "EU 44", "EU 45"]},
        {"id": 26, "name": "Foreign Fashionable Half Shoe", "price": 17000.00, "image": "/static/s16.jpg", "options": ["EU 40", "EU 41", "EU 42", "EU 43", "EU 44", "EU 45"]},
        {"id": 27, "name": "Classic Men's Foreign Half Shoe", "price": 25000.00, "image": "/static/s17.jpg", "options": ["EU 40", "EU 41", "EU 42", "EU 43", "EU 44", "EU 45"]},
        {"id": 28, "name": "NEW ARRIVAL SUEDE TIE BLACK SHOE", "price": 17000.00, "image": "/static/s18.jpg", "options": ["EU 40", "EU 41", "EU 42", "EU 43", "EU 44", "EU 45"]},
        {"id": 29, "name": "Gentleman's Casual Frosted Men Leather Shoes - Black", "price": 38990.00, "image": "/static/s19.jpg", "options": ["EU 40", "EU 41", "EU 42", "EU 43", "EU 44", "EU 45"]},
        {"id": 30, "name": "Vangelo NEW VANGELO LUXURY CORPORATE AND WEDDING DESIGNER MEN'S SHOE BROWN", "price": 27500.00, "image": "/static/s20.jpg", "options": ["EU 40", "EU 41", "EU 42", "EU 43", "EU 44", "EU 45"]}
    ],
    "wristwatches": [
        {"id": 31, "name": "DS Stone Iced Mens Wristwatch Hand Chain", "price": 20000.00, "image": "/static/w1.jpg", "options": ["Adults", "Teenager"]},
        {"id": 32, "name": "Wrist Watche Fashion Iuminous Waterproof Simple Quartz Watch Gold/Brown", "price": 10000.00, "image": "/static/w2.jpg", "options": ["Adults", "Teenager"]},
        {"id": 33, "name": "ARHANORY Men's Quartz Watches Business Wristwatch Stylish - Black", "price": 10000.00, "image": "/static/w3.jpg", "options": ["Adults", "Teenager"]},
        {"id": 34, "name": "VERY ICY! ICE-BOX Studded Chain Watch + Sophisticated ICY Armlet For Boss", "price": 50000.00, "image": "/static/w4.jpg", "options": ["Adults", "Teenager"]},
        {"id": 35, "name": "2 IN 1 Men's Watch Fashion Waterproof Sport Quartz Business Watch", "price": 10000.00, "image": "/static/w5.jpg", "options": ["Adults", "Teenager"]},
        {"id": 36, "name": "Men Non Tarnish Gold Watch + Cuban Handchain", "price": 13990.00, "image": "/static/w6.jpg", "options": ["Adults", "Teenager"]},
        {"id": 37, "name": "BLAZE Full Touch Screen Watch - For Android & IOS", "price": 10990.00, "image": "/static/w7.jpg", "options": ["Adults", "Teenager"]},
        {"id": 38, "name": "Men Brown Silicon Wristwatch", "price": 7990.00, "image": "/static/w8.jpg", "options": ["Adults", "Teenager"]},
        {"id": 39, "name": "Mens Digital Watch Wrist Watches With Date LED Stopwatch", "price": 20500.00, "image": "/static/w9.jpg", "options": ["Adults", "Teenager"]},
        {"id": 40, "name": "Binbond Men's Fashion Mechanical Watch Waterproof Night Light Reinforced Wrist Watches - Bronze", "price": 30811.00, "image": "/static/w10.jpg", "options": ["Adults", "Teenager"]}
    ]
}

# Home Route
@app.route('/')
def index():
    return render_template('index.html', products=products)

# Contact Form Route
@app.route('/contact', methods=['POST'])
def contact():
    name = request.form.get('name')
    email = request.form.get('email')
    message = request.form.get('message')

    if not name or not email or not message:
        return render_template('index.html', products=products, error="All fields are required!", message_sent=False)

    # Here you can add logic to handle the contact form (e.g., send an email, save to database)
    return render_template('index.html', products=products, message_sent=True)

# Paystack Payment Route - Create Checkout Session
@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    data = request.get_json()
    product_id = data.get('productId')
    selected_option = data.get('size')  # Update this to match the form field
    email = data.get("email", "customer@example.com")

    product = None
    for category, items in products.items():
        for item in items:
            if item['id'] == int(product_id):  # Convert product_id to int
                product = item
                break
        if product:
            break

    if not product:
        return jsonify({'error': 'Product not found'}), 404

    if not selected_option and product.get("options") and len(product.get("options")) > 0:
        return jsonify({'error': 'Please select an option'}), 400

    try:
        response = paystack.transaction.initialize(
            amount=int(product['price'] * 100),
            email=email,
            reference=f'contour_{product_id}_{int(os.urandom(8).hex(), 16)}',
            callback_url='https://coutour.onrender.com/verify-payment',
            metadata={"option": selected_option or ""}
        )

        if response['status']:
            return jsonify({'payment_url': response['data']['authorization_url']})
        else:
            return jsonify({'error': 'Failed to initialize payment'}), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Route for Address Submission
@app.route('/submit_address', methods=['POST'])
def submit_address():
    product_id = request.form.get('product_id')
    selected_option = request.form.get('option')
    full_name = request.form.get('full_name')
    address_line1 = request.form.get('address_line1')
    address_line2 = request.form.get('address_line2')
    city = request.form.get('city')
    state = request.form.get('state')
    postal_code = request.form.get('postal_code')
    phone = request.form.get('phone')
    email = request.form.get('email', "customer@example.com")

    # Basic validation
    if not all([product_id, full_name, address_line1, city, state, postal_code, phone, email]):
        return jsonify({'error': 'All required fields must be filled'}), 400

    product = next((item for category in products.values() for item in category if item['id'] == int(product_id)), None)
    if not product:
        return jsonify({'error': 'Product not found'}), 404

    if not selected_option and product.get("options") and len(product.get("options")) > 0:
        return jsonify({'error': 'Please select an option'}), 400

    try:
        # Store address details in session (optional, for later use)
        session['order_details'] = {
            'product_id': product_id,
            'option': selected_option,
            'full_name': full_name,
            'address_line1': address_line1,
            'address_line2': address_line2,
            'city': city,
            'state': state,
            'postal_code': postal_code,
            'phone': phone,
            'email': email
        }

        # Initialize Paystack transaction with address metadata
        response = paystack.transaction.initialize(
            amount=int(product['price'] * 100),
            email=email,
            reference=f'contour_{product_id}_{int(os.urandom(8).hex(), 16)}',
            callback_url='https://coutour.onrender.com/verify-payment',
            metadata={
                "option": selected_option or "",
                "full_name": full_name,
                "address_line1": address_line1,
                "address_line2": address_line2 or "",
                "city": city,
                "state": state,
                "postal_code": postal_code,
                "phone": phone
            }
        )

        if response['status']:
            return jsonify({'payment_url': response['data']['authorization_url']})
        else:
            return jsonify({'error': 'Failed to initialize payment'}), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Verify Payment Route
@app.route('/verify-payment')
def verify_payment():
    reference = request.args.get('reference')
    if not reference:
        return redirect(url_for('index', _anchor='cancel'))

    try:
        response = paystack.transaction.verify(reference=reference)
        if response['status'] and response['data']['status'] == 'success':
            # Payment successful, you can save order details here
            session.pop('order_details', None)  # Clear session after successful payment
            return redirect(url_for('index', _anchor='success'))
        else:
            return redirect(url_for('index', _anchor='cancel'))
    except Exception as e:
        return redirect(url_for('index', _anchor='cancel'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.getenv('PORT', 5000)))