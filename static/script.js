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

        // Redirect to Stripe Checkout (supports Mastercard and Verve)
        stripe.redirectToCheckout({ sessionId: data.sessionId }).then(result => {
            if (result.error) {
                alert(`Payment error: ${result.error.message}`);
            }
        });
    } catch (error) {
        alert(`Failed to initiate payment: ${error.message}`);
        console.error("Payment error:", error);
    }
}