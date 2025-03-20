// Show the address form and pass the product ID
function showAddressForm(productId) {
    console.log(`showAddressForm called with Product ID: ${productId}`);
    const sizeSelect = document.querySelector(`.size-select[data-product-id="${productId}"]`);
    const selectedSize = sizeSelect ? sizeSelect.value : null;

    console.log(`Product ID: ${productId}, Size Select Element:`, sizeSelect, `Selected Size: ${selectedSize}`);

    // Only prompt for size if the product has a size dropdown, has more than one option, and no size is selected
    if (sizeSelect && sizeSelect.options.length > 1 && selectedSize === "") {
        // Remove any existing error messages
        const existingError = sizeSelect.parentElement.querySelector('.error-message');
        if (existingError) {
            existingError.remove();
        }

        // Create and display an inline error message
        const errorDiv = document.createElement('div');
        errorDiv.className = 'error-message';
        errorDiv.textContent = 'Please select a size before proceeding.';
        sizeSelect.parentElement.appendChild(errorDiv);
        setTimeout(() => errorDiv.remove(), 3000);
        return;
    }

    // Store product ID and size in the form
    document.getElementById('product-id').value = productId;
    document.getElementById('selected-size').value = selectedSize || '';

    console.log(`Navigating to address section for Product ID: ${productId}`);
    showSection('address');
}

// Handle address form submission and initiate Paystack payment
async function submitOrder(event) {
    event.preventDefault();
    const form = event.target;
    const formData = new FormData(form);

    try {
        const response = await fetch('/submit_address', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (data.error) {
            const formError = document.createElement('div');
            formError.className = 'error-message';
            formError.textContent = `Error: ${data.error}`;
            form.appendChild(formError);
            setTimeout(() => formError.remove(), 3000);
            return;
        }

        window.location.href = data.payment_url;
    } catch (error) {
        console.error('Error during address submission:', error);
        const formError = document.createElement('div');
        formError.className = 'error-message';
        formError.textContent = 'An error occurred while processing your address. Please try again.';
        form.appendChild(formError);
        setTimeout(() => formError.remove(), 3000);
    }
}

// Show a specific section and hide others
function showSection(sectionId) {
    console.log(`showSection called with sectionId: ${sectionId}`);
    const sections = document.querySelectorAll('.section');
    sections.forEach(section => {
        section.style.display = 'none';
    });
    const section = document.getElementById(sectionId);
    if (section) {
        section.style.display = 'block';
    } else {
        console.error(`Section with ID ${sectionId} not found`);
    }
}

// Auto-scrolling carousel logic
document.addEventListener('DOMContentLoaded', () => {
    showSection('home');

    // Carousel setup
    const carousel = document.getElementById('product-carousel');
    const images = carousel.querySelectorAll('img');
    const indicatorsContainer = document.getElementById('carousel-indicators');
    let currentIndex = 0;

    // Create indicators
    images.forEach((_, index) => {
        const indicator = document.createElement('span');
        indicator.addEventListener('click', () => {
            currentIndex = index;
            updateCarousel();
        });
        indicatorsContainer.appendChild(indicator);
    });

    function updateCarousel() {
        carousel.style.transform = `translateX(-${currentIndex * 100}%)`;
        const indicators = indicatorsContainer.querySelectorAll('span');
        indicators.forEach((indicator, index) => {
            indicator.classList.toggle('active', index === currentIndex);
        });
    }

    // Auto-scroll every 3 seconds
    setInterval(() => {
        currentIndex = (currentIndex + 1) % images.length;
        updateCarousel();
    }, 3000);

    // Initial update
    updateCarousel();

    // Add event listeners to all size select dropdowns
    const sizeSelects = document.querySelectorAll('.size-select');
    sizeSelects.forEach(select => {
        const productId = select.getAttribute('data-product-id');
        const buyButton = document.querySelector(`.buy-now[data-product-id="${productId}"]`);

        if (buyButton) {
            if (select.options.length > 1) {
                buyButton.disabled = true;
                console.log(`Disabled Buy Now button for Product ID: ${productId} (size selection required)`);
            } else {
                buyButton.disabled = false;
                console.log(`Enabled Buy Now button for Product ID: ${productId} (no size selection required)`);
            }

            select.addEventListener('change', function() {
                const existingError = this.parentElement.querySelector('.error-message');
                if (existingError) {
                    existingError.remove();
                }
                buyButton.disabled = this.value === "";
                console.log(`Buy Now button for Product ID: ${productId} is now ${buyButton.disabled ? 'disabled' : 'enabled'}`);
            });
        }
    });

    // Ensure buttons for products without sizes are clickable
    const buyButtons = document.querySelectorAll('.buy-now');
    buyButtons.forEach(button => {
        const productId = button.getAttribute('data-product-id');
        const sizeSelect = document.querySelector(`.size-select[data-product-id="${productId}"]`);
        if (!sizeSelect || sizeSelect.options.length <= 1) {
            button.disabled = false;
            console.log(`Ensured Buy Now button is enabled for Product ID: ${productId} (no size dropdown or single option)`);
        } else {
            console.log(`Buy Now button for Product ID: ${productId} remains disabled (size dropdown exists)`);
        }
    });

    // Toggle hamburger menu
    const hamburger = document.querySelector('.hamburger');
    const navLinks = document.querySelector('.nav-links');
    hamburger.addEventListener('click', () => {
        navLinks.classList.toggle('active');
        hamburger.classList.toggle('open');
    });
});