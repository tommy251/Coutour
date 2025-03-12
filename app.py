from flask import Flask, jsonify, render_template, send_from_directory, request, redirect, url_for
import logging
import stripe

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)

# Configure Stripe (replace with your Stripe keys)
stripe.api_key = "your_stripe_secret_key"  # Replace with your Stripe secret key
stripe_public_key = "your_stripe_public_key"  # Replace with your Stripe public key

# Manual product catalog
products = {
    "clothes": [
        {"id": 1, "name": "Basic T-Shirt", "price": 5.99, "image": "/static/images/tshirt.jpg", "description": "Comfortable cotton t-shirt, available in multiple colors."},
        {"id": 2, "name": "Workout Leggings", "price": 12.99, "image": "/static/images/leggings.jpg", "description": "Stretchable leggings for gym or casual wear."}
    ],
    "shoes": [
        {"id": 3, "name": "Running Shoes", "price": 19.99, "image": "/static/images/runningshoes.jpg", "description": "Lightweight shoes for running and training."}
    ],
    "wristwatches": [
        {"id": 4, "name": "Classic Watch", "price": 9.99, "image": "/static/images/watch.jpg", "description": "Stylish analog watch with leather strap."}
    ]
}

# Serve the index.html file at the root URL
@app.route("/")
def serve_index():
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
            return "Product not found", 404
        
        # Create a Stripe Checkout Session
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{
                "price_data": {
                    "currency": "usd",
                    "product_data": {"name": product["name"]},
                    "unit_amount": int(product["price"] * 100),  # Convert to cents
                },
                "quantity": 1,
            }],
            mode="payment",
            success_url=url_for("success", _external=True),
            cancel_url=url_for("cancel", _external=True),
        )
        return jsonify({"sessionId": session.id})
    except Exception as e:
        logger.error(f"Failed to create Stripe session: {e}")
        return jsonify({"error": str(e)}), 500

@app.route("/success")
def success():
    return render_template("success.html")

@app.route("/cancel")
def cancel():
    return render_template("cancel.html")

if __name__ == "__main__":
    # Only run the development server if this script is executed directly
    app.run(host="0.0.0.0", port=5000, debug=True)