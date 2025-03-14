async function orderProduct(productId) {
    try {
        // Get the selected size from the dropdown
        const sizeSelect = document.querySelector(`.size-select[data-product-id="${productId}"]`);
        const selectedSize = sizeSelect ? sizeSelect.value : null;

        if (selectedSize === "" && sizeSelect) { // Check if size is required and not selected
            alert('Please select a size before checking out.');
            return;
        }

        // Step 1: Fetch the payment URL from your server
        const response = await fetch('/create-checkout-session', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ productId: productId, size: selectedSize }),
        });

        const data = await response.json();

        if (data.error) {
            alert('Error: ' + data.error);
            return;
        }

        // Step 2: Redirect to Paystack's payment page
        window.location.href = data.payment_url;
    } catch (error) {
        console.error('Error during checkout:', error);
        alert('An error occurred while processing your order. Please try again.');
    }
}