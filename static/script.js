async function orderProduct(productId) {
    try {
        const response = await fetch(`/pay/${productId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        const data = await response.json();
        
        if (data.error) {
            alert(`Error: ${data.error}`);
            return;
        }

        // Redirect to Stripe Checkout
        stripe.redirectToCheckout({ sessionId: data.sessionId });
    } catch (error) {
        alert(`Failed to initiate payment: ${error.message}`);
        console.error("Payment error:", error);
    }
}