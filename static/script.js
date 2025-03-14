// Ensure Stripe is loaded (if using Stripe for international payments)
const stripe = Stripe(window.stripePublicKey);

// Function to handle product ordering
async function orderProduct(productId) {
    try {
        // Step 1: Fetch the checkout session from your server
        const response = await fetch('/create-checkout-session', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ productId: productId }),
        });

        const session = await response.json();

        if (session.error) {
            alert('Error: ' + session.error);
            return;
        }

        // Step 2: Redirect to the payment gateway's checkout page
        const result = await stripe.redirectToCheckout({
            sessionId: session.id
        });

        if (result.error) {
            alert('Payment Error: ' + result.error.message);
        }
    } catch (error) {
        console.error('Error during checkout:', error);
        alert('An error occurred while processing your order. Please try again.');
    }
}