// Initialize Stripe with the public key from the global variable
console.log('Initializing Stripe with public key:', window.stripePublicKey);
const stripe = Stripe(window.stripePublicKey);

async function orderProduct(productId) {
    console.log('Ordering product with ID:', productId);
    try {
        const response = await fetch(`/pay/${productId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        console.log('Fetch response status:', response.status);
        const data = await response.json();
        console.log('Fetch response data:', data);
        
        if (data.error) {
            alert(`Error: ${data.error}`);
            return;
        }

        // Redirect to Stripe Checkout (supports Mastercard and Verve)
        stripe.redirectToCheckout({ sessionId: data.sessionId }).then(result => {
            if (result.error) {
                alert(`Payment error: ${result.error.message}`);
                console.error('Stripe error:', result.error);
            }
        });
    } catch (error) {
        alert(`Failed to initiate payment: ${error.message}`);
        console.error("Payment error:", error);
    }
}