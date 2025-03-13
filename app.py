from flask import Flask, jsonify, render_template, send_from_directory, request, redirect, url_for
import logging
import stripe
import os

# Configure Stripe using environment variables
stripe.api_key = os.getenv("STRIPE_SECRET_KEY", "your_stripe_secret_key")  # Fallback for local testing
stripe_public_key = os.getenv("STRIPE_PUBLIC_KEY", "your_stripe_public_key")  # Fallback for local testing

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
        {"id": 1, "name": "Basic T-Shirt", "price": 1999.00, "image": "/static/images/tshirt.jpg", "description": "Comfortable cotton t-shirt, available in multiple colors."},
        {"id": 2, "name": "Workout Leggings", "price": 4999.00, "image": "/static/images/leggings.jpg", "description": "Stretchable leggings for gym or casual wear."}
    ],
    "shoes": [
        {"id": 3, "name": "Running Shoes", "price": 7999.00, "image": "/static/images/runningshoes.jpg", "description": "Lightweight shoes for running and training."}
    ],
    "wristwatches": [
        {"id": 4, "name": "Classic Watch", "price": 3999.00, "image": "/static/images/watch.jpg", "description": "Stylish analog watch with leather strap."}
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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)