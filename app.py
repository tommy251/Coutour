from flask import Flask, jsonify, render_template, send_from_directory, request, redirect, url_for
import logging
import stripe
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)

# Configure Stripe using environment variables
stripe.api_key = os.getenv("STRIPE_SECRET_KEY", "your_stripe_secret_key")
stripe_public_key = os.getenv("STRIPE_PUBLIC_KEY", "your_stripe_public_key")

# Email configuration (Gmail SMTP)
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS", "your-email@gmail.com")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD", "your-app-password")
RECIPIENT_EMAIL = os.getenv("RECIPIENT_EMAIL", "your-email@gmail.com")  # Your email to receive messages

# Manual product catalog
products = {
    "Clothes": [
        {"id": 1, "name": "Trendy Offwhite Up And Down Wears", "price": 20,000.00, "image": "/static/c1.jpg", "description": "S | M |L | XL | XXL | XXXL | XXXL."}
        {"id": 2, "name": "Custom-Made Trendy Up And Down Wears 2", "price": 20,000.00, "image": "/static/c2.jpg", "description": "S | M |L | XL | XXL | XXXL | XXXL."},
        {"id": 3, "name": "Trendy Blue Up And Down Wears Pk2", "price": 20,000.00, "image": "/static/c3.jpg", "description": "S | M |L | XL | XXL | XXXL | XXXL."},
        {"id": 4, "name": "4 IN 1 UNISEX COLLAR N PLAIN ROUND NECK T-SHIRT POLO SHIRT FOR MEN", "price": 25,000.00, "image": "/static/c4.jpg", "description": "S | M |L | XL | XXL | XXXL | XXXL."},
        {"id": 5, "name": "Men`s 3 In 1 Sleeveless Hoodie T-Shirts For Gym & Sport - Multi", "price": 20,000.00, "image": "/static/c5.jpg", "description": "S | M |L | XL | XXL | XXXL | XXXL."},
        {"id": 6, "name": "Classic Watch", "price": 3999.00, "image": "/static/c6.jpg", "description": "S | M |L | XL | XXL | XXXL | XXXL."},
        {"id": 7, "name": "Classic Watch", "price": 3999.00, "image": "/static/c7.jpg", "description": "S | M |L | XL | XXL | XXXL | XXXL."},
        {"id": 8, "name": "Classic Watch", "price": 3999.00, "image": "/static/c8.jpg", "description": "S | M |L | XL | XXL | XXXL | XXXL."},
        {"id": 9, "name": "Classic Watch", "price": 3999.00, "image": "/static/c9.jpg", "description": "S | M |L | XL | XXL | XXXL | XXXL."},
        {"id": 10, "name": "Classic Watch", "price": 3999.00, "image": "/static/c10.jpg", "description": "S | M |L | XL | XXL | XXXL | XXXL."}
    ],
    "Shoes": [
        {"id": 1, "name": "Men'S Lightweight Shoes - Casual Athletic Sneakers - Black Canvas", "price": 8999.00, "image": "/static/s1.jpg", "Size": "EU 40, EU 41, EU 43, EU 44."},
        {"id": 2, "name": "DEPALLY ROUND STONE DESIGNERS SHOE BLACK", "price": 28,980.00, "image": "/static/s2.jpg", "Size": "EU 40, EU 41, EU 42, EU 43, EU 44,EU 45"},
        {"id": 3, "name": "Men'S Trendy Men's Outdoor Sport Lace-up Casual Comfortable Sneakers - Canvas - Size", "price": 20,000.00, "image": "/static/s3.jpg", "Size": " EU 43, EU 44"},
        {"id": 4, "name": "Men'S Men Fashion Quality Outdoor comfortable Casual Shoes": 20,999.00, "image": "/static/s4.jpg", "Size": "EU 43, EU 44"},
        {"id": 5, "name": "Canvas Men's Casual Simple Sport Fashion Sneakers - Comfortable Shoes", "price": 8,980.00, "image": "/static/s5.jpg", "Size": "EU 39, EU 40, EU 44"},
        {"id": 6, "name": "Men Leather Shoes Oxford Wedding Corporate Formal Loafers Slip-Ons Vintage Brown", "price": 29,500.00, "image": "/static/s6.jpg", "Size": "EU 40, EU 41, EU 42, EU 43, EU 44,EU 45"},
        {"id": 7, "name": "Depally Men's Brogue Tie Designers Shoe Black", "price": 32,000.00, "image": "/static/s7.jpg", "Size": "EU 40, EU 41, EU 42, EU 43, EU 44,EU 45"},
        {"id": 8, "name": "Men's Leather Shoes Large Size-Black", "price": 16,980.00, "image": "/static/s8.jpg", "Size": "EU 40, EU 41, EU 42, EU 43, EU 44,EU 45"},
        {"id": 9, "name": "Men's Formal Italian Wedding Brogues Leather Shoes Lace Up Brown", "price": 27,900.00, "image": "/static/s9.jpg", "Size": "EU 40, EU 41, EU 42, EU 43, EU 44,EU 45"},
        {"id": 10, "name": "Men'S 2024 Men's Casual Simple Board Sport Running Shoes - Fashion Outdoor Shoes", "price": 8,999.00, "image": "/static/s10.jpg", "Size": "EU 40, EU 41, EU 42, EU 43, EU 44,EU 45"},
        {"id": 11, "name": "DEPALLY ROUND STONE DESIGNERS SHOE BLACK", "price": 28,980.00, "image": "/static/s11.jpg", "Size": "EU 40, EU 41, EU 42, EU 43, EU 44,EU 45"},
        {"id": 12, "name": "DEPALLY ROUND STONE DESIGNERS SHOE BLACK", "price": 28,980.00, "image": "/static/s12.jpg", "Size": "EU 40, EU 41, EU 42, EU 43, EU 44,EU 45"},
        {"id": 13, "name": "DEPALLY ROUND STONE DESIGNERS SHOE BLACK", "price": 28,980.00, "image": "/static/s13.jpg", "Size": "EU 40, EU 41, EU 42, EU 43, EU 44,EU 45"},
        {"id": 14, "name": "DEPALLY ROUND STONE DESIGNERS SHOE BLACK", "price": 28,980.00, "image": "/static/s14.jpg", "Size": "EU 40, EU 41, EU 42, EU 43, EU 44,EU 45"},
        {"id": 15, "name": "DEPALLY ROUND STONE DESIGNERS SHOE BLACK", "price": 28,980.00, "image": "/static/s15.jpg", "Size": "EU 40, EU 41, EU 42, EU 43, EU 44,EU 45"},
        {"id": 16, "name": "DEPALLY ROUND STONE DESIGNERS SHOE BLACK", "price": 28,980.00, "image": "/static/s16.jpg", "Size": "EU 40, EU 41, EU 42, EU 43, EU 44,EU 45"},
        {"id": 17, "name": "DEPALLY ROUND STONE DESIGNERS SHOE BLACK", "price": 28,980.00, "image": "/static/s17.jpg", "Size": "EU 40, EU 41, EU 42, EU 43, EU 44,EU 45"},
        {"id": 18, "name": "DEPALLY ROUND STONE DESIGNERS SHOE BLACK", "price": 28,980.00, "image": "/static/s18.jpg", "Size": "EU 40, EU 41, EU 42, EU 43, EU 44,EU 45"},
        {"id": 19, "name": "DEPALLY ROUND STONE DESIGNERS SHOE BLACK", "price": 28,980.00, "image": "/static/s19.jpg", "Size": "EU 40, EU 41, EU 42, EU 43, EU 44,EU 45"},
        {"id": 20, "name": "DEPALLY ROUND STONE DESIGNERS SHOE BLACK", "price": 28,980.00, "image": "/static/s20.jpg", "Size": "EU 40, EU 41, EU 42, EU 43, EU 44,EU 45"}
    ],
    "wristwatches": [
        {"id": 1, "name": "DS Stone Iced Mens Wristwatch Hand Chain", "price": 20,000.00, "image": "/static/w1.jpg", "description": "Stylish analog watch with leather strap."}
        {"id": 2, "name": "Wrist Watche Fashion Iuminous Waterproof Simple Quartz Watch Gold/Brown", "price": 10,000.00, "image": "/static/w2.jpg", "description": "Stylish analog watch with leather strap."},
        {"id": 3, "name": "ARHANORY Men's Quartz Watches Business Wristwatch Stylish - Black", "price": 10,000.00, "image": "/static/w3.jpg", "description": "Stylish analog watch with leather strap."},
        {"id": 4, "name": "VERY ICY! ICE-BOX Studded Chain Watch + Sophisticated ICY Armlet For Boss", "price": 50,000.00, "image": "/static/4.jpg", "description": "Stylish analog watch with leather strap."},
        {"id": 5, "name": "2 IN 1 Men's Watch Fashion Waterproof Sport Quartz Business Watch", "price": 10,000.00, "image": "/static/w5.jpg", "description": "Stylish analog watch with leather strap."},
        {"id": 6, "name": "Classic Watch", "price": 3999.00, "image": "/static/w6.jpg", "description": "Stylish analog watch with leather strap."},
        {"id": 7, "name": "Classic Watch", "price": 3999.00, "image": "/static/w7.jpg", "description": "Stylish analog watch with leather strap."},
        {"id": 8, "name": "Classic Watch", "price": 3999.00, "image": "/static/w8.jpg", "description": "Stylish analog watch with leather strap."},
        {"id": 9, "name": "Classic Watch", "price": 3999.00, "image": "/static/w9.jpg", "description": "Stylish analog watch with leather strap."},
        {"id": 10, "name": "Classic Watch", "price": 3999.00, "image": "/static/w10.jpg", "description": "Stylish analog watch with leather strap."}
    ]
}

# Serve the index.html file at the root URL
@app.route("/")
@app.route("/<section>")
def serve_index(section=None):
    try:
        logger.debug("Attempting to render index.html")
        return render_template("index.html", products=products, stripe_public_key=stripe_public_key)
    except Exception as e:
        logger.error(f"Failed to render index.html: {e}")
        return "Error rendering template", 500

# Serve static files
@app.route("/static/<path:path>")
def serve_static(path):
    try:
        logger.debug(f"Serving static file: {path}")
        return send_from_directory("static", path)
    except Exception as e:
        logger.error(f"Failed to serve static file {path}: {e}")
        return "Error serving static file", 500

# Payment route for Stripe
@app.route("/pay/<int:product_id>", methods=["POST"])
def pay(product_id):
    try:
        product = next((item for category in products.values() for item in category if item["id"] == product_id), None)
        if not product:
            return jsonify({"error": "Product not found"}), 404
        
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{
                "price_data": {
                    "currency": "ngn",
                    "product_data": {"name": product["name"], "description": product["description"]},
                    "unit_amount": int(product["price"] * 100),
                },
                "quantity": 1,
            }],
            mode="payment",
            success_url=url_for("serve_index", section="success", _external=True),
            cancel_url=url_for("serve_index", section="cancel", _external=True),
            metadata={"product_id": str(product_id), "brand": "Contour"},
        )
        return jsonify({"sessionId": session.id})
    except Exception as e:
        logger.error(f"Failed to create Stripe session: {e}")
        return jsonify({"error": str(e)}), 500

# Contact form route
@app.route("/contact", methods=["POST"])
def contact():
    try:
        # Get form data
        name = request.form["name"]
        email = request.form["email"]
        message = request.form["message"]

        # Create email content
        msg = MIMEMultipart()
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = RECIPIENT_EMAIL
        msg["Subject"] = f"New Contact Form Submission from {name}"
        body = f"Name: {name}\nEmail: {email}\nMessage: {message}"
        msg.attach(MIMEText(body, "plain"))

        # Send email via Gmail SMTP
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, RECIPIENT_EMAIL, msg.as_string())

        logger.debug("Email sent successfully")
        return render_template("index.html", products=products, stripe_public_key=stripe_public_key, message_sent=True)

    except Exception as e:
        logger.error(f"Failed to send email: {e}")
        return render_template("index.html", products=products, stripe_public_key=stripe_public_key, message_sent=False, error=str(e))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)